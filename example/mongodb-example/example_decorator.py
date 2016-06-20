# import mongodb driver
import pymongo
import time

# import python-cache pycache package
from pycache.Adapter import MongoItemPool
from pycache import cached

# create mongo client
client = pymongo.MongoClient(host="192.168.99.100", port=27017)

# init MongoItemPool with Mongo client
pool = MongoItemPool(client)


# decorate myAdder function in common way
@cached(CacheItemPool=pool)
def myAdder(a, b):
    import time
    print 'Add %d + %d need 3 seconds!' % (a, b)
    time.sleep(3)
    return a+b


print(myAdder(5, 6)) # wait for 3 seconds
print(myAdder(5, 6)) # no need wait
