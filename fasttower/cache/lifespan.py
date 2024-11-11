from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi_cache import FastAPICache

from fasttower.conf import settings
from fasttower.server import FastTower
from fasttower.utils import get_class


@asynccontextmanager
async def cache_lifespan(_: FastTower) -> AsyncIterator[None]:
    FastAPICache.init(get_class(settings.CACHE['default']['BACKEND'])(),
                      prefix=settings.CACHE['default'].get("prefix", "fasttower-cache"))
    yield
