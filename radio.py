import redis, time, random, math, datetime

if __name__ == "__main__":
    r = redis.StrictRedis('localhost', 6379, decode_responses=True)
    x = 0
    start_time = time.time()
    while True:
        comm = r.rpop('commands')
        if(comm is not None):
            if(comm=='abort'):
                start_time = time.time()
        t = -(start_time-time.time())

        r.rpush('data:timeOfFlight', t)
        r.rpush('data:height', (t * .5))
        r.rpush('data:pressure', abs(math.sin(t)))
        # time.sleep(.001)