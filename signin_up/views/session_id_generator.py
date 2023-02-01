import datetime
import json
import random
import string
from flask import Response
import redis
from model.all_model import User, redis_instance


def error_control(function):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            function(self)
        except Exception as e:  # Todo: implement for every case and every status code
            # log here
            self.response = Response(json.dumps({"response": str(e)}),
                                     status=400,
                                     mimetype='application/json')

    return wrapper


class SessionId:
    def __init__(self):
        self.new_user_id = None
        self.sessionId = None
        self.response = None
        self.engine()

    @error_control
    def engine(self):
        self.publish_session_id()

    def publish_session_id(self):
        # new_user = User(user_timestamp=datetime.datetime.utcnow(),
        #                 user_id='U__' + ''.join(random.choices(string.ascii_lowercase +
        #                                                        string.digits, k=14)))
        # new_user.save()
        self.sessionId = ''.join(random.choices(string.ascii_lowercase +
                                                string.digits, k=14))
        redis_instance.setex(str(self.sessionId), 86400, str(datetime.datetime.utcnow()))
        self.response = Response(json.dumps({"response": f"{self.sessionId}"}), status=200,
                                 mimetype="application/json")
