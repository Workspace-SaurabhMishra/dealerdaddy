from model.all_model import redis_instance

x = redis_instance

for i in redis_instance.keys(pattern="*"):
    print(i)
    redis_instance.delete(i)
