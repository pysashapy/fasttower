from fastapi_cache.decorator import cache

from fasttower.cache.backends import RedisBackend, InMemoryBackend

__all__ = [
    'cache',
    "RedisBackend",
    "InMemoryBackend"
]
