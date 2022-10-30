import datetime
import json
import random
import string
from flask import Response
import redis
from signin_up.model.all_model import User


def error_control(function):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            function(self)
        except Exception as e:  # Todo: implement for every case and every status code
            #log here
            self.response = Response(json.dumps({"response": str(e)}),
                                     status=400,
                                     mimetype='application/json')

    return wrapper


class SessionId:
    def __init__(self):
        self.redis_instance = None
        self.sessionId = None
        self.response = None
        self.engine()

    @error_control
    def engine(self):
        self.init_redis()
        self.publish_session_id()

    def init_redis(self):
        self.redis_instance = redis.Redis(host="127.0.0.1", port=6379, db=0)

    def publish_session_id(self):
        new_user = User(user_timestamp=datetime.datetime.utcnow(),
                        user_id='U__' + ''.join(random.choices(string.ascii_lowercase +
                                                               string.digits, k=14)))
        new_user.save()
        self.sessionId = new_user.user_id
        self.redis_instance.set(str(self.sessionId), str(datetime.datetime.utcnow()))
        self.response = Response(json.dumps({"response": f"{self.sessionId}"}), status=200,
                                 mimetype="application/json")
