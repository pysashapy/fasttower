"""
ASGI config for example project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

from fasttower.utils import setup, lifespans

os.environ.setdefault("FASTTOWER_SETTINGS_MODULE", "example.settings")
setup()

from fasttower.server import FastTower

from example.routers import router
from fasttower.admin.site import app as admin_app, lifespan_admin
from fasttower.db import lifespan

app = FastTower(title="FastTower API Documentation", lifespan=lifespans([lifespan, lifespan_admin]))

app.mount('/admin', admin_app)

app.include_router(router)
