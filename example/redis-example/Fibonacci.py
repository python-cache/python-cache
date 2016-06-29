# import redis driver
import redis
import pymongo

# import python-cache pycache package
from pycache.Adapter import RedisItemPool
from pycache.Adapter import MongoItemPool
from pycache import cached

client = redis.Redis(host='192.168.99.100', port=32771)
pool = RedisItemPool(client)

mongo_client = pymongo.MongoClient(host="192.168.99.100", port=27017)
mongo_pool = MongoItemPool(mongo_client)

def fib(num):
    if num == 1 or num == 0:
        return num
    return fib(num-1) + fib(num-2)

@cached(CacheItemPool=pool)
def cached_fib(num):
    if num == 1 or num == 0:
        return num
    return cached_fib(num - 1) + cached_fib(num - 2)

@cached(CacheItemPool=mongo_pool)
def mongo_cached_fib(num):
    if num == 1 or num == 0:
        return num
    return mongo_cached_fib(num - 1) + mongo_cached_fib(num - 2)


from datetime import datetime
for i in range(1, 50):
    cur = datetime.utcnow()
    fib(i)
    diff = (datetime.utcnow() - cur)
    nocached = float(diff.seconds) + float(diff.microseconds) / 1000000

    cur = datetime.utcnow()
    cached_fib(i)
    diff = (datetime.utcnow() - cur)
    cached = float(diff.seconds) + float(diff.microseconds) / 1000000
    pool.clear()

    cur = datetime.utcnow()
    mongo_cached_fib(i)
    diff = (datetime.utcnow() - cur)
    mongo_cached = float(diff.seconds) + float(diff.microseconds) / 1000000
    mongo_pool.clear()



    print i, nocached, cached, mongo_cached