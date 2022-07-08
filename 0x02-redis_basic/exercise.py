#!/usr/bin/env python3
"""Defines a class Cache."""
import uuid
import redis
from functools import wraps
from typing import Callable, Optional, Union


def count_calls(method: Callable) -> Callable:
    """Decorator to count number of times methods of Cache class are called."""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper of decorator"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """Handles caching."""

    def __init__(self):
        """Intanciates a new Cache."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generates random key and store the arg data in it."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        """Gets data from the cache."""
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Converts redis data to string."""
        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """Converts redis data to int."""
        data = self._redis.get(key)
        return int(data)
