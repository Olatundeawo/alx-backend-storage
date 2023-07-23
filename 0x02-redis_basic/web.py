#!/usr/bin/env python3
"""
Redis using a python script
"""
import redis
from requests import get
from typing import Callable
from functools import wraps


redis_store = redis.Redis()


def use_callable(method: Callable) -> Callable:
    """using a functool"""
    @wraps(method)
    def invoker(url: str) -> str:
        '''The wrapper function for caching the output.
        '''
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@use_callable
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    return get(url).text
