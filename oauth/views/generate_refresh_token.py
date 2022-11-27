import datetime
import json
import random
import string

from flask import Response

from oauth.model.all_model import redis_instance_refresh_rw, redis_instance_refresh_r, redis_instance_access_rw


class GenerateRefreshToken:
    def __init__(self):
        self.datetime = datetime.datetime.utcnow()
        self.refresh_token = ''.join(random.choices(string.ascii_lowercase +
                                                    string.digits, k=14))
        self.access_token = ''.join(random.choices(string.ascii_lowercase +
                                                   string.digits, k=14))
        self.response = Response(json.dumps({
            "refresh_token": self.refresh_token,
            "access_token": self.access_token
        }), status=200, mimetype="application/json")

        self.engine()

    def engine(self):
        self.persist_token()

    def persist_token(self):
        redis_instance_refresh_rw.setex(self.refresh_token, 100, str(self.datetime))
        redis_instance_refresh_r.setex(self.refresh_token, 100, str(self.datetime))
        redis_instance_access_rw.setex(self.refresh_token, 100, str(self.datetime))
