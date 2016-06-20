# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
"""CacheItem.

This module defines an interface for interacting with objects inside a cache.

"""
from abc import ABCMeta, abstractmethod

class CacheItemInterface():

    def get_key(self):
        """Returns the key for the current cache item.

        Note:
            The key is loaded by the Implementing Library, but should be available to
            the higher level callers when needed.

        :return The key string for this cache item.

        """
        pass

    def get(self):
        """Retrieves the value of the item from the cache associated with this object's key.

        Note:
            The value returned must be identical to the value originally stored by set().

            If isHit() returns false, this method MUST return null. Note that null
            is a legitimate cached value, so the isHit() method SHOULD be used to
            differentiate between "null value was found" and "no value was found."

        :return The value corresponding to this cache item's key, or null if not found.

        """
        pass

    def is_hit(self):
        """Confirms if the cache item lookup resulted in a cache hit.

        Note:
            This method MUST NOT have a race condition between calling isHit()
            and calling get().

        :return True if the request resulted in a cache hit. False otherwise.

        """
        pass

    def set(self, key, value):
        """Sets the key and value represented by this cache item.

        Note:
            The $value argument may be any item that can be serialized by python,
            although the method of serialization is left up to the Implementing
            Library.

        Args:
            value: The serializable value to be stored.

        :return The invoked object.

        """
        pass


    def expires_at(self, timestamp):
        """Sets the expiration time for this cache item.

        Note:
            The point in time after which the item MUST be considered expired.
            If null is passed explicitly, a default value MAY be used. If none is set,
            the value should be stored permanently or for as long as the
            implementation allows.

        :param time: expiration time in timestamp

        :return The called object.

        """
        pass

    def expires_after(self, seconds):
        """Sets the expiration time for this cache item.

        Note:
            The period of time from the present after which the item MUST be considered
            expired. An integer parameter is understood to be the time in seconds until
            expiration. If null is passed explicitly, a default value MAY be used.
            If none is set, the value should be stored permanently or for as long as the
            implementation allows.

        :param time: expiration time in timedelta

        :return The called object.

        """
        pass
