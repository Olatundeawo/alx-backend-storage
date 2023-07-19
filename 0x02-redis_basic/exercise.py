#!/usr/bin/env python3
"""
A class file with type-annotate python
"""
import redis
import uuid
from typing import Any, Callable, Optional, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Get the number of calls made to a method in a cache
        class
    """
    @wraps(method)
    def start(self, *arg, **kwargs) -> Any:
        """Method that start the call incrementing"""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *arg, **kwargs)
    return start


def call_history(method: Callable) -> Callable:
    """Store the input and output"""
    @wraps(method)
    def get_history(self, *arg, **kwarg) -> Any:
        '''Return the input and output method'''
        input_key = '{}:inputs'.format(method.__qualname__)
        output_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(arg))
        output = method(self, *arg, **kwarg)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, output)
        return output
    return get_history


def replay(fn: Callable) -> None:
    '''Displays the call history of a Cache class' method.
    '''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


class Cache:
    """ A cache class"""
    def __init__(self) -> None:
        """ starting the cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
