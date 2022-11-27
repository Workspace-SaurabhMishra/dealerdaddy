import redis


class RedisInstance:
    redis_instance_refresh_rw = None
    redis_instance_refresh_r = None
    redis_instance_access_rw = None

    def __init__(self):
        self.redis_instance_refresh_rw = redis.Redis(host="127.0.0.1", port=6379, db=1)  # TOdo: set keys for some time
        self.redis_instance_refresh_r = redis.Redis(host="127.0.0.1", port=6379, db=2)  # TOdo: set keys for some time
        self.redis_instance_access_rw = redis.Redis(host="127.0.0.1", port=6379, db=3)  # TOdo: set keys for some time


redis_instance_refresh_rw = RedisInstance().redis_instance_refresh_rw
redis_instance_refresh_r = RedisInstance().redis_instance_refresh_r
redis_instance_access_rw = RedisInstance().redis_instance_access_rw
