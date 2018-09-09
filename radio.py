import redis, time, random, math, datetime

if __name__ == "__main__":
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    x = 0
    start_time = time.time()
    while True:
        if(r.exists('abort')):
            start_time = time.time()
            r.delete('abort')

        vz = 10
        x = -(start_time-time.time())
        r.rpush('data:height', x)
        # time.sleep(.001)