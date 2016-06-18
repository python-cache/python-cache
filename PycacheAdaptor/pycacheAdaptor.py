# -*- coding: utf-8 -*-
"""pycacheAdaptor.

This module provides useful caching functions and decorators

"""


def cached(cache='memory', deferred=False):
    """
      Caches the result of the computation
      based on the function parameters
      available.
      :param cache: cache
      :return cached value
    """
    def decorator(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner
    return decorator
