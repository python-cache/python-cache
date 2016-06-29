import cPickle
import redis
from datetime import datetime

from pycache.Adapter.CacheItemPoolInterface import CacheItemPoolInterface
from pycache.cacheItem import CacheItem
from pycache.settings import PREFIX as prefix

# -*- coding: utf-8 -*-
"""
RedisItemPool.

This module generates CacheItemInterface objects.

"""


class RedisItemPool(CacheItemPoolInterface):

    def __init__(self, client=redis.Redis(host='localhost',port=6379), PREFIX=prefix):
        self.client = client
        self.key_prefix = PREFIX+":"

    def get_item(self, key):
        """Returns a Cache Item representing the specified key.

        Note:
            This method must always return a CacheItemInterface object, even in case of
            a cache miss. It MUST NOT return null.

        :param key: The key for which to return the corresponding Cache Item.

        :exception CacheException: If the `key` string is not a legal value

        :return The corresponding Cache Item.

        """

        if self.has_item(key):
            key = self.normalize_key(key)
            item_str = self.client.get(key)
            item = cPickle.loads(item_str)
            item.isHit = True
            return item
        else:
            item = CacheItem()

            item.key = key
            return item


    def get_items(self, keys=None):
        """Returns a traversable set of cache items.

        :param keys: An indexed array of keys of items to retrieve.

        :exception CacheException: If any of the keys in `keys` are not a legal value

        :return
            A traversable collection of Cache Items keyed by the cache keys of
            each item. A Cache item will be returned for each key, even if that
            key is not found. However, if no keys are specified then an empty
            traversable MUST be returned instead.

        """
        items = []
        for key in keys:
            items.append(self.get_item(key))
        return items


    def has_item(self, key):
        """Confirms if the cache contains specified cache item.

        Note:
            This method MAY avoid retrieving the cached value for performance reasons.
            This could result in a race condition with CacheItemInterface::get(). To avoid
            such situation use CacheItemInterface::isHit() instead.

        :param key: The key for which to check existence.

        :exception CacheException: If any of the keys in `keys` are not a legal value

        :return True if item exists in the cache, false otherwise.

        """
        return self.client.exists(self.normalize_key(key))


    def clear(self):
        """Deletes all items in the pool.

        :return True if the pool was successfully cleared. False if there was an error.

        """
        return self.client.flushall()


    def delete_item(self, key):
        """Removes the item from the pool.

        :param key: The key for which to delete

        :exception CacheException: If any of the keys in `keys` are not a legal value

        :return True if the item was successfully removed. False if there was an error.

        """
        return self.client.delete(self.normalize_key(key))


    def save(self, item):
        """Persists a cache item immediately.

        :param item: The cache item to save.

        :return True if the item was successfully persisted. False if there was an error.

        """

        if item.expire_at != datetime.max:
            expire_seconds = (item.expire_at - datetime.utcnow()).seconds
            if expire_seconds > 0:
                return self.client.setex(self.normalize_key(item.key),
                                     cPickle.dumps(item), expire_seconds)
            else:
                return False
        else:
            return self.client.set(self.normalize_key(item.key),
                                   cPickle.dumps(item))


    def save_deferred(self, item):
        """Sets a cache item to be persisted later.

        :param item: The cache item to save.

        :return False if the item could not be queued or if a commit was attempted and failed. True otherwise.

        """
        return False


    def commit(self):
        """Persists any deferred cache items.

        :return True if all not-yet-saved items were successfully saved or there were none. False otherwise.

        """
        return True

    def normalize_key(self, key):
        return self.key_prefix+cPickle.dumps(key)
