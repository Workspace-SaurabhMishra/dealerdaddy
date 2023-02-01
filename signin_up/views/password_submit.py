import json
import typing

import redis
from flask import Response
from marshmallow import fields, Schema, utils

from signin_up.model.all_model import User, redis_instance


def password_verification_validator(function):
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
        self.session_user = redis_instance.get(self.session_id)
        if self.session_user is None or len(self.session_user) == 0:
            self.response = Response(json.dumps({"response": "invalid process"}), status=400,
                                     mimetype="application/json")
            # {reminder}report false signup attempt
            return
        else:
            temp = User.objects(password=self.password)
            if len(temp) == 1:
                self.response = Response(json.dumps({"response": "password already exist"}), status=400,
                                         mimetype="application/json")
            elif len(temp) >= 2:
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
    password = CustomStringField(required=True)
    # Todo: Do something about empty string


class EnterPassword:
    def __init__(self, payload):
        self.session_user = None
        self.redis_result = None
        self.payload = payload
        self.phone_number = payload.get("phone_number")
        self.password = payload.get("password")
        self.session_id = payload.get("session_id")
        self.response = self.response = Response(json.dumps({"response": "something went wrong"}), status=500,
                                                 mimetype="application/json")

        self.engine()

    # @error_control
    @password_verification_validator
    @duplicate_user
    def engine(self):
        self.persist_password()

    def persist_password(self):
        self.redis_result = redis_instance.get(f"{self.phone_number}")
        if len(self.redis_result.decode()) == 1:
            self.session_user = User.objects(user_id="U__"+self.session_id)[0]
            self.session_user["password"] = self.phone_number
            self.session_user.save()
            self.response = Response(json.dumps({"response": "success"}), status=200,
                                     mimetype="application/json")
        else:
            self.response = Response(json.dumps({"response": "enter phone number first"}), status=401,
                                     mimetype="application/json")