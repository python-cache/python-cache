import cPickle
import pymongo
from datetime import datetime

from pycache.Adapter.CacheItemPoolInterface import CacheItemPoolInterface
from pycache.cacheItem import CacheItem
from pycache.settings import PREFIX

# -*- coding: utf-8 -*-
"""
MongoItemPool.

This module generates CacheItemInterface objects.

"""


class MongoItemPool(CacheItemPoolInterface):

    def __init__(self, client = pymongo.MongoClient(host="localhost", port=27017), DB="pycache", COLLECTION=PREFIX):
        self.client = client
        self.collection = self.client[DB][COLLECTION]
        self.collection.create_index("expireAt", expireAfterSeconds=0)

    def get_item(self, key):
        """Returns a Cache Item representing the specified key.

        Note:
            This method must always return a CacheItemInterface object, even in case of
            a cache miss. It MUST NOT return null.

        :param key: The key for which to return the corresponding Cache Item.

        :exception CacheException: If the `key` string is not a legal value

        :return The corresponding Cache Item.

        """
        key = self.normalize_key(key)
        document = self.collection.find_one({"key": key})
        if document != None:

            item = cPickle.loads(str(document['item']))
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
        key = self.normalize_key(key)
        document = self.collection.find_one({"key": key})
        if document != None:
            return True
        else:
            return False


    def clear(self):
        """Deletes all items in the pool.

        :return True if the pool was successfully cleared. False if there was an error.

        """
        return self.collection.remove({})


    def delete_item(self, key):
        """Removes the item from the pool.

        :param key: The key for which to delete

        :exception CacheException: If any of the keys in `keys` are not a legal value

        :return True if the item was successfully removed. False if there was an error.

        """
        return self.collection.remove({"key":self.normalize_key(key)})


    def save(self, item):
        """Persists a cache item immediately.

        :param item: The cache item to save.

        :return True if the item was successfully persisted. False if there was an error.

        """

        if item.expire_at != datetime.max:
            if item.expire_at > datetime.utcnow():
                return self.collection.update(
                    {"key": self.normalize_key(item.key)},
                    {"key": self.normalize_key(item.key),
                    "item": cPickle.dumps(item),
                    "expireAt": item.expire_at },
                    upsert=True)
            else:
                return False
        else:
            return self.collection.update(
                {"key": self.normalize_key(item.key)},
                {"key": self.normalize_key(item.key),
                "item": cPickle.dumps(item)},
                upsert=True)


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
        return cPickle.dumps(key)
