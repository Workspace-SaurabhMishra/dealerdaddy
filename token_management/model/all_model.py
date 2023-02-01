import redis


class RedisInstance:
    redis_instance_access = None
    redis_instance_refresh = None

    def __init__(self):
        self.redis_instance_access = redis.Redis(host="127.0.0.1", port=6379, db=0)  # TOdo: set keys for some time
        self.redis_instance_refresh = redis.Redis(host="127.0.0.1", port=6379, db=0)  # TOdo: set keys for some time


redis_instance_access = RedisInstance().redis_instance_access
redis_instance_refresh = RedisInstance().redis_instance_refresh
