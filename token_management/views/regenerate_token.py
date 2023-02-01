import datetime
import json
import random
import string

from flask import Response

from token_management.model.all_model import redis_instance_refresh, redis_instance_access


class AccessToken:
    def __init__(self):
        self.new_access_token = None
        self.access_token = None
        self.refresh_token = None
        self.datetime = datetime.datetime.utcnow()
        self.response = Response(json.dumps({
            "response": "internal server error"
        }), status=500, mimetype="application/json")

        self.engine()

    def engine(self):
        self.access_token()

    def access_token(self):
        if redis_instance_refresh.get(str(self.refresh_token)) not in (None, ""):
            self.new_access_token = ''.join(random.choices(string.ascii_lowercase +
                                                           string.digits, k=14))
            redis_instance_access.setex(self.access_token, 3600, str(self.datetime))
            self.response = Response(json.dumps({
                "response": "valid token",
                "access_token": str(self.new_access_token)
            }), status=200, mimetype="application/json")
            self.persist_token()
        else:
            self.response = Response(json.dumps({
                "response": "invalid token"
            }), status=498, mimetype="application/json")

    def persist_token(self):
        redis_instance_access.setex(self.new_access_token, 3600, str(self.datetime))
        self.response = Response(json.dumps({
            "refresh_token": self.refresh_token,
            "access_token": self.access_token
        }), status=200, mimetype="application/json")
