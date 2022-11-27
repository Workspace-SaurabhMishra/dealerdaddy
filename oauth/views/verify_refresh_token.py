import datetime
import json

from flask import Response

from oauth.model.all_model import redis_instance_refresh_rw, redis_instance_refresh_r, \
    redis_instance_access_rw


class VerifyTokens:
    def __init__(self, payload):
        self.payload = payload
        self.access_token = payload.get("access_token")
        self.refresh_token = payload.get("refresh_token")
        self.response = Response(json.dumps({
            "response": "invalid token"
        }), status=400, mimetype="application/json")

        self.engine()

    def engine(self):
        self.verify_token()

    def verify_token(self):
        if redis_instance_access_rw.get(str(self.access_token)) not in (None, ""):
            self.response = Response(json.dumps({
                "response": "valid token"
            }), status=200, mimetype="application/json")
        else:
            if redis_instance_refresh_rw.get(str(self.refresh_token)) in (None, "") and redis_instance_refresh_r.get(
                    str(self.refresh_token)) not in (None, ""):
                redis_instance_refresh_rw.setex(self.refresh_token, 300, str(datetime.datetime.utcnow()))
                self.response = Response(json.dumps({
                    "response": "valid token"
                }), status=200, mimetype="application/json")
            else:
                redis_instance_access_rw.setex(self.access_token, 120, str(datetime.datetime.utcnow()))
                self.response = Response(json.dumps({
                    "response": "valid token"
                }), status=200, mimetype="application/json")
