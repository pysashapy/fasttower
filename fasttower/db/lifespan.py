# pylint: disable=E0611,E0401
from contextlib import asynccontextmanager
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise
from typing import AsyncGenerator

from fasttower.conf import settings


async def initialize_tortoise():
    await Tortoise.init(config=settings.DATABASES)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with RegisterTortoise(app, config=settings.DATABASES, generate_schemas=True):
        yield
