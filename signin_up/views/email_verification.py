import json
import typing
from datetime import datetime

import redis
from flask import Response
from marshmallow import Schema, fields, utils

from model.all_model import User, redis_instance


def email_payload_validator(function):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            EmailVerificationSchema().load(self.payload)
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
            print(e)
            self.response = Response(json.dumps({"response": str(e)}),
                                     status=400,
                                     mimetype='application/json')

    return wrapper


def duplicate_user(function):
    def wrapper(*args, **kwargs):
        self = args[0]
        self.session_user = redis_instance.get(self.session_id)
        print(self.session_user)
        if len(self.session_user) == 0:
            self.response = Response(json.dumps({"response": "invalid process"}), status=400,
                                     mimetype="application/json")
            # {reminder}report false signup attempt
            return
        else:
            temp = User.objects(email=self.email)
            if len(temp) == 1:
                self.response = Response(json.dumps({"response": "email address exist"}), status=400,
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


class EmailVerificationSchema(Schema):
    session_id = CustomStringField(required=True)
    email = CustomStringField(required=True)
    otp = CustomStringField(required=True)
    # Todo: Do something about empty string


class EmailVerification:
    def __init__(self, payload):
        self.session_user = None
        self.redis_result = None
        self.payload = payload
        self.otp = payload.get("otp")
        self.email = payload.get("email")
        self.session_id = payload.get("session_id")
        self.response = self.response = Response(json.dumps({"response": "something went wrong"}), status=500,
                                                 mimetype="application/json")

        self.engine()

    @error_control
    @email_payload_validator
    @duplicate_user
    def engine(self):
        self.persist_email()

    def persist_email(self):
        self.redis_result = redis_instance.get(f"{self.email}")
        if self.redis_result.decode() == self.otp:
            self.session_user = User(user_id="U__" + self.session_id, user_timestamp=datetime.utcnow())
            self.session_user["email"] = self.email
            self.session_user.save()
            self.response = Response(json.dumps({"response": "otp verified"}), status=200,
                                     mimetype="application/json")
        else:
            self.response = Response(json.dumps({"response": "wrong otp"}), status=401,
                                     mimetype="application/json")
