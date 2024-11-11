"""
ASGI config for example project.

It exposes the ASGI callable as a module-level variable named ``app``.
"""

import os

from fasttower.utils import setup

os.environ.setdefault("FASTTOWER_SETTINGS_MODULE", "example.settings")
setup()

from fasttower.server import FastTower

from fasttower.utils import lifespans
from fasttower.cache.lifespan import cache_lifespan
from fasttower.db.lifespan import tortoise_lifespan

from example.routers import router

app = FastTower(title="FastTower API Documentation", lifespan=lifespans([tortoise_lifespan, cache_lifespan]))

app.include_router(router)