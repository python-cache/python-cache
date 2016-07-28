# import redis driver
import redis
import time

# import python-cache pycache package
from pycache.Adapter import RedisItemPool
from pycache import CacheItem

# create redis client
client = redis.Redis(host='192.168.99.100', port=6379)

# init RedisItemPool with redis client
pool = RedisItemPool(client)
item = CacheItem()


# A common way to do key-val caching

item.set("mykey","myval")
pool.save(item)
ret_item = pool.get_item("mykey")
print(ret_item.get(), ret_item.get_key()) # "mykey", "myval"

print("--")

# set expire
item.set("mykey","myval")
item.expire_after(1)
print("sleep 2 seconds")
time.sleep(2)
print("isHit:",item.is_hit()) # "False"
pool.save(item)
ret_item = pool.get_item("mykey")
print(ret_item.is_hit(), ret_item.get(), ret_item.get_key())