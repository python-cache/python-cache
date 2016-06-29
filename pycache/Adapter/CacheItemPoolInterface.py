# -*- coding: utf-8 -*-
"""CacheItemPoolInterface.

This module generates CacheItemInterface objects.

"""

from abc import ABCMeta, abstractmethod


class CacheItemPoolInterface(dict):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __len__(self):
        """Returns the number of CacheItem in the pool.

        :return: return the number of CacheItem in the pool
        """
        pass

    @abstractmethod
    def __getitem__(self, key):
        """Returns a Cache Item representing the specified key.

        Note:
            This method must always return a CacheItemInterface object, even in case of
            a cache miss. It MUST NOT return null.

        :param key: The key for which to return the corresponding Cache Item.

        :exception CacheException: If the `key` string is not a legal value

        :return The corresponding Cache Item.

        """
        pass

    @abstractmethod
    def __contains__(self, key):
        """Confirms if the cache contains specified cache item.

        Note:
            This method MAY avoid retrieving the cached value for performance reasons.
            This could result in a race condition with CacheItemInterface::get(). To avoid
            such situation use CacheItemInterface::isHit() instead.

        :param key: The key for which to check existence.

        :exception CacheException: If any of the keys in `keys` are not a legal value

        :return True if item exists in the cache, false otherwise.

        """
        pass

    @abstractmethod
    def clear(self):
        """Deletes all items in the pool.

        :return True if the pool was successfully cleared. False if there was an error.

        """
        pass

    @abstractmethod
    def __delitem__(self, key):
        """Removes the item from the pool.

        :param key: The key for which to delete

        :exception CacheException: If any of the keys in `keys` are not a legal value

        :return True if the item was successfully removed. False if there was an error.

        """
        pass

    @abstractmethod
    def __setitem__(self, key, value):
        """Persists a cache item immediately.

        :param item: The cache item to save.

        :return True if the item was successfully persisted. False if there was an error.

        """
        pass

    @abstractmethod
    def save_deferred(self, item):
        """Sets a cache item to be persisted later.

        :param item: The cache item to save.

        :return False if the item could not be queued or if a commit was attempted and failed. True otherwise.

        """
        pass

    @abstractmethod
    def commit(self):
        """Persists any deferred cache items.

        :return True if all not-yet-saved items were successfully saved or there were none. False otherwise.

        """
        pass
