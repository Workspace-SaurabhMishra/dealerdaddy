import json
import typing

import redis
from flask import Response
from marshmallow import fields, Schema, utils

from model.all_model import User


def mobile_verification_validator(function):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            MobileVerificationSchema().load(self.payload)
        except Exception as e:
            self.response = Response(json.dumps("{0}".format(e)),
                                     status=400,
                                     mimetype='application/json')
            return
        function(self)

    return wrapper


def error_control(function):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            function(self)
        except Exception as e:  # Todo: implement for every case and every status code
            self.response = Response(json.dumps({"response": str(e)}),
                                     status=400,
                                     mimetype='application/json')

    return wrapper


def duplicate_user(function):
    def wrapper(*args, **kwargs):
        self = args[0]
        self.session_user = User.objects(user_id=self.session_id)
        if len(self.session_user) == 0:
            self.response = Response(json.dumps({"response": "invalid process"}), status=400,
                                     mimetype="application/json")
            # {reminder}report false signup attempt
            return
        else:
            temp = User.objects(phone_number=self.phone_number)
            if len(temp) == 1:
                self.response = Response(json.dumps({"response": "phone number address exist"}), status=400,
                                         mimetype="application/json")
            elif len(temp) == 2:
                pass
                # {reminder} report duplicate data in DB
            else:
                function(self)

    return wrapper


class CustomStringField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs) -> typing.Any:
        if not isinstance(value, (str, bytes)) or value == "":
            raise self.make_error("invalid")
        try:
            return utils.ensure_text_type(value)
        except UnicodeDecodeError as error:
            raise self.make_error("invalid_utf8") from error


class MobileVerificationSchema(Schema):
    session_id = CustomStringField(required=True)
    phone_number = CustomStringField(required=True)
    otp = CustomStringField(required=True)
    # Todo: Do something about empty string


class MobileVerification:
    def __init__(self, payload):
        self.session_user = None
        self.redis_result = None
        self.redis_instance = None
        self.payload = payload
        self.otp = payload.get("otp")
        self.phone_number = payload.get("phone_number")
        self.session_id = payload.get("session_id")
        self.response = self.response = Response(json.dumps({"response": "something went wrong"}), status=500,
                                                 mimetype="application/json")

        self.engine()

    @error_control
    @mobile_verification_validator
    @duplicate_user
    def engine(self):
        self.init_redis()
        self.persist_phone_number()

    def init_redis(self):
        self.redis_instance = redis.Redis(host="127.0.0.1", port=6379, db=0)

    def persist_phone_number(self):
        self.redis_result = self.redis_instance.get(f"{self.phone_number}")
        if self.redis_result.decode() == self.otp:
            self.session_user = User.objects(user_id=self.session_id)[0]
            self.session_user["phone_number"] = self.phone_number
            self.session_user.save()
            self.response = Response(json.dumps({"response": "otp verified"}), status=200,
                                     mimetype="application/json")
        else:
            self.response = Response(json.dumps({"response": "wrong otp"}), status=401,
                                     mimetype="application/json")
