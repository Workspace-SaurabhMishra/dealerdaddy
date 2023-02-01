import datetime
import json
import random
import string

from flask import Response

from token_management.model.all_model import redis_instance_refresh, redis_instance_access


class GenerateToken:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.datetime = datetime.datetime.utcnow()
        self.response = Response(json.dumps({
            "refresh_token": self.refresh_token,
            "access_token": self.access_token
        }), status=200, mimetype="application/json")

        self.engine()

    def refresh_token(self):
        self.refresh_token = ''.join(random.choices(string.ascii_lowercase +
                                                    string.digits, k=14))

    def access_token(self):
        self.access_token = ''.join(random.choices(string.ascii_lowercase +
                                                   string.digits, k=14))

    def engine(self):
        self.access_token()
        self.refresh_token()
        self.persist_token()

    def persist_token(self):
        redis_instance_access.setex(self.access_token, 3600, str(self.datetime))
        redis_instance_refresh.setx(self.refresh_token, 86400, str(self.datetime))
