import settings

from pycache.Adapter import MongoItemPool
from pycache import CacheItem
from pycache.cacheDecorator import cached
import pymongo
import time


class TestCacheItem():

    def test_simpleKeyVal(self):
        # create mongo client
        client = pymongo.MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)

        # init MongoItemPool with Mongo client
        pool = MongoItemPool(client, DB="pycache", COLLECTION="pytest")
        item = CacheItem()

        item.set("mykey", "myval")
        pool.save(item)
        ret_item = pool.get_item("mykey")
        assert ret_item.get() == "myval"
        assert ret_item.get_key() == "mykey"
        assert ret_item.is_hit() == True

    def test_expire_atfter(self):
        # create mongo client
        client = pymongo.MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)

        # init MongoItemPool with Mongo client
        pool = MongoItemPool(client, DB="pycache", COLLECTION="pytest")
        item = CacheItem()

        # set expire
        item.set("mykey", "myval")
        item.expires_after(1)
        pool.save(item)
        ret_item = pool.get_item("mykey")
        assert ret_item.is_hit() == True

        time.sleep(2)
        ret_item = pool.get_item("mykey")
        assert ret_item.is_hit() == False

    def test_Decorator(self):
        client = pymongo.MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)
        pool = MongoItemPool(client, DB="pycache", COLLECTION="pytest")

        # decorate myAdder function in common way
        @cached(CacheItemPool=pool)
        def myAdder(a, b):
            import time
            print 'Add %d + %d need 3 seconds!' % (a, b)
            time.sleep(3)
            return a + b

        assert myAdder(5, 6) == 11  # wait for 3 seconds
        assert myAdder(5, 6) == 11  # no need wait
