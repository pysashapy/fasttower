# pylint: disable=E0611,E0401
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise

from fasttower.conf import settings


async def initialize_tortoise():
    await Tortoise.init(config=settings.DATABASES)


@asynccontextmanager
async def tortoise_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    from fasttower.conf import settings
    async with RegisterTortoise(
            app,
            config=settings.DATABASES,
            generate_schemas=True,
            add_exception_handlers=True,
    ):
        yield
