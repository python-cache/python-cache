import settings

from pycache import CacheItem
import time



class TestCacheItem():

    def test_simpleKeyVal(self):
        item = CacheItem()
        item.set("mykey", "myval")
        assert item.get() == "myval"
        assert item.get_key() == "mykey"
        assert item.is_hit() == True

    def test_expire_after(self):
        item = CacheItem()
        item.set("mykey", "myval")
        assert item.get() == "myval"
        assert item.get_key() == "mykey"
        assert item.is_hit() == True
        item.expires_after(0.5)
        time.sleep(1)
        assert item.is_hit() == False