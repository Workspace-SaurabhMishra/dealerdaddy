import json
import smtplib
import random
import string
import typing
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import redis
from flask import Response
from marshmallow import Schema, fields, validate, utils

from model.all_model import User, redis_instance


def signin_payload_validator(function):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            SignInRequestSchema().load(self.payload)
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


class CustomStringField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs) -> typing.Any:
        if not isinstance(value, (str, bytes)) or value == "":
            raise self.make_error("invalid")
        try:
            return utils.ensure_text_type(value)
        except UnicodeDecodeError as error:
            raise self.make_error("invalid_utf8") from error


class SignInRequestSchema(Schema):
    username = CustomStringField(required=True)
    password = CustomStringField(required=True)
    # Todo: Do something about empty string


class SignIn:
    def __init__(self, request_payload):
        self.payload = request_payload
        self.username = request_payload.get("username")
        self.password = request_payload.get("password")

    @error_control
    @signin_payload_validator
    def engine(self):
        self.check_credentials()

    def check_credentials(self):
        pass

