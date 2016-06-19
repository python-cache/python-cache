# import redis driver
import redis

# import python-cache pycache package
from pycache.Adapter import RedisItemPool
from pycache import CacheItem

# create redis client
client = redis.Redis(host='192.168.99.100', port=32769)

# init RedisItemPool with redis client
pool = RedisItemPool(client)

# A common way to do key-val caching
item = CacheItem()
item.set("mykey","myval")
pool.save(item)
ret_item = pool.get_item("mykey")
print(ret_item.get(), ret_item.get_key())