# import redis driver
import redis

# import python-cache pycache package
from pycache.Adapter import RedisItemPool
from pycache import cached


# create redis client
client = redis.Redis(host='192.168.99.100', port=32771)

# init RedisItemPool with redis client
pool = RedisItemPool(client)


# decorate myAdder function in common way
@cached(CacheItemPool=pool)
def myAdder(a, b):
    import time
    print 'Add %d + %d need 3 seconds!' % (a, b)
    time.sleep(3)
    return a+b


print(myAdder(5, 6)) # wait for 3 seconds
print(myAdder(5, 6)) # no need wait
