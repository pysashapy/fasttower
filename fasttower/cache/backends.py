from fastapi_cache.backends.inmemory import InMemoryBackend as _InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend as _RedisBackend
from redis import asyncio as aioredis

from fasttower.conf import settings


class RedisBackend(_RedisBackend):
    def __init__(self, config="default"):
        super().__init__(
            aioredis.from_url(settings.CACHE[config]["LOCATION"])
        )


class InMemoryBackend(_InMemoryBackend):
    def __init__(self, config="default"):
        super().__init__()
