import datetime

from model.all_model import redis_instance_refresh_rw, redis_instance_access_rw, redis_instance_refresh_r

print("#############  1.Refresh Tokens  ############")
for i in redis_instance_refresh_rw.keys(pattern="*"):
    print(i)

print("#############  2.Refresh Tokens  ############")
for i in redis_instance_refresh_r.keys(pattern="*"):
    print(i)

print("#############  Access Tokens  ############")
for i in redis_instance_access_rw.keys(pattern="*"):
    print(i)
