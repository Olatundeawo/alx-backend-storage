#!/usr/bin/env python3
"""
A class file with type-annotate python
"""
import redis
import uuid
from typing import Any, Callable, Optional, Union


class Cache:
    """ A cache class"""
    def __init__(self, _redis):
        """ starting the cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Any) -> str:
        """ store data in the cache"""
        rand = str(uuid.uuid4())
        self._redis.set(rand, data)
        return rand

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ Get data from the cache"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_int(self, key: str) -> int:
        """ Get an int value from the cache"""
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value

    def get_str(self, key: str) -> str:
        """ get a string value"""
        value = self._redis.get(key)
        return value.decode('utf-8')
