import redis

r = redis.StrictRedis()

print(r.lpop('data:height'))