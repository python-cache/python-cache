# import mongodb driver
import pymongo
import time

# import python-cache pycache package
from pycache.Adapter import MongoItemPool
from pycache import CacheItem

# create mongo client
client = pymongo.MongoClient(host="192.168.99.100", port=27117)

# init MongoItemPool with Mongo client
pool = MongoItemPool(client, DB="ANA", COLLECTION="Test")
item = CacheItem()

# ---A common way to do key-val caching---
print("---Simple Key Val---")

item.set("mykey","myval")
pool.save(item)
ret_item = pool.get_item("mykey")
print(ret_item.get(), ret_item.get_key())
# ("mykey", "myval")


# ---expire before save---
print("---expire before save---")
item.set("mykey","myval")
item.expires_after(1)
print("sleep 2 seconds")
time.sleep(2)
print("isHit:",item.is_hit()) # "False"
pool.save(item)

ret_item = pool.get_item("mykey")
print(ret_item.is_hit(), ret_item.get(), ret_item.get_key())
# (False, None, "mykey")


# ---save then expire---
print("---save then expire---")
item.set("mykey","myval")
item.expires_after(1)
pool.save(item)
print("sleep 2 seconds")
time.sleep(2)

ret_item = pool.get_item("mykey")
print(ret_item.is_hit(), ret_item.get(), ret_item.get_key())
# (False,  None, 'mykey')
