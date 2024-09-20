from tortoise.exceptions import DoesNotExist

from fasttower.db import models
from fasttower.db.lifespan import lifespan, initialize_tortoise
from fasttower.exceptions import NotFoundException

__all__ = [
    'initialize_tortoise',
    'models',
    "lifespan",
    "get_object_or_404",
]


async def get_object_or_404(queryset, **kwargs):
    try:
        return await queryset.get(**kwargs)
    except DoesNotExist:
        raise NotFoundException()
