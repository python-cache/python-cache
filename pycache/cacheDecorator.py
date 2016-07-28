# -*- coding: utf-8 -*-
"""pycacheAdaptor.

This module provides useful caching functions and decorators

"""
import cPickle

from pycache.cacheItem import CacheItem

def cached(CacheItemPool='memory',
           enable=True,
           expire_after=None,
           expire_at=None):
    """
      Caches the result of the computation
      based on the function parameters
      available.
      :param cache: cache
      :return cached value
    """
    def decorator(func):
        def inner(*args, **kwargs):
            # Cache Closed
            if enable != True:
                return func(*args, **kwargs)

            # Cache Opened
            key = (func.__name__, cPickle.dumps(args), cPickle.dumps(kwargs))
            item = CacheItemPool.get_item(key)
            if item.is_hit():
                val = item.get()
            else:
                val = func(*args, **kwargs)
                item = CacheItem()
                item.set(key, val)
                if expire_after != None:
                    item.expire_after(expire_after)
                if expire_at != None:
                    item.expire_at(expire_at)
                CacheItemPool.save(item)
            return val
        return inner
    return decorator


# def cached(cache='memory', deferred=False):
#     """
#       Caches the result of the computation
#       based on the function parameters
#       available.
#       :param cache: cache
#       :return cached value
#     """
#     def decorator(func):
#         def inner(*args, **kwargs):
#             return func(*args, **kwargs)
#         return inner
#     return decorator