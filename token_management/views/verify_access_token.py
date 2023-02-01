import datetime
import json

from flask import Response

from token_management.model.all_model import redis_instance_access, redis_instance_refresh


class VerifyToken:
    def __init__(self, payload):
        self.new_access_token = None
        self.payload = payload
        self.datetime = datetime.datetime.utcnow()
        self.access_token = payload.get("access_token")
        self.refresh_token = payload.get("refresh_token")
        self.response = Response(json.dumps({
            "response": "internal server error"
        }), status=500, mimetype="application/json")

        self.engine()

    def engine(self):
        self.verify_token()

    def verify_token(self):
        if redis_instance_access.get(str(self.access_token)) not in (None, ""):
            self.response = Response(json.dumps({
                "response": "valid token",
                "access_token": str(self.access_token)
            }), status=200, mimetype="application/json")
        else:
            self.response = Response(json.dumps({
                "response": "invalid token"
            }), status=498, mimetype="application/json")
