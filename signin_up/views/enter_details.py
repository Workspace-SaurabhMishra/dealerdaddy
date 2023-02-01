import json
import os
import random
import string
import sys
import typing

import plivo
import redis

from flask import Response
from marshmallow import Schema, fields, utils

from model.all_model import User, redis_instance


def details_payload_validator(function):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            MobileRequestSchema().load(self.payload)
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


# def duplicate_user(function):
#     def wrapper(*args, **kwargs):
#         self = args[0]
#         self.session_user = redis_instance.get(self.session_id)
#         if self.session_user is None or len(self.session_user) == 0:
#             self.response = Response(json.dumps({"response": "invalid process"}), status=400,
#                                      mimetype="application/json")
#             # {reminder}report false signup attempt
#             return
#         else:
#             temp = User.objects(phone_number=self.phone_number)
#             if len(temp) == 1:
#                 self.response = Response(json.dumps({"response": "phone number address exist"}), status=400,
#                                          mimetype="application/json")
#             elif len(temp) == 2:
#                 pass
#                 # {reminder} report duplicate data in DB
#             else:
#                 function(self)
#
#     return wrapper


class CustomStringField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs) -> typing.Any:
        if not isinstance(value, (str, bytes)) or value == "":
            raise self.make_error("invalid")
        try:
            return utils.ensure_text_type(value)
        except UnicodeDecodeError as error:
            raise self.make_error("invalid_utf8") from error


class MobileRequestSchema(Schema):
    session_id = CustomStringField(required=True)
    name = CustomStringField(required=True)
    dob = CustomStringField(required=True)
    gender = CustomStringField(required=True)
    address = CustomStringField(required=True)
    # Todo: Do something about empty string


class MobileSubmit:
    def __init__(self, payload):
        self.session_user = None
        self.create_message = None
        self.payload = payload
        self.name = payload.get('name')
        self.dob = payload.get('dob')
        self.address = payload.get('address')
        self.session_id = payload.get('session_id')
        # self.otp = ''.join(random.choices(string.digits, k=4))
        self.otp = "1234"
        self.response = Response(json.dumps({"response": "Something went wrong"}), status=500,
                                 mimetype="application/json")
        self.engine()
    # @error_control
    @details_payload_validator
    # @duplicate_user
    def engine(self):
        self.

    def
