from contextlib import asynccontextmanager, AsyncExitStack
from importlib import import_module
from typing import Type, List, Callable

from fastapi import FastAPI
from tortoise import timezone
from tortoise.contrib.fastapi import register_tortoise as register_orm


def get_module(path: str):
    try:
        path, module = path.rsplit(':', maxsplit=1)
        print(path, module)
        module = getattr(import_module(path), module)
    except ModuleNotFoundError as e:
        raise e
    except ValueError:
        raise ImportError('Module not be imported')
    return module


def get_user_model() -> Type['AbstractUser']:
    from fasttower.conf import settings
    return get_module(settings.USER_MODEL)


def lifespans(lifespans_: List[Callable]):
    @asynccontextmanager
    async def _lifespan_manager(app: FastAPI):
        exit_stack = AsyncExitStack()
        async with exit_stack:
            for lifespan_ in lifespans_:
                await exit_stack.enter_async_context(lifespan_(app))
            yield

    return _lifespan_manager


def setup():
    from fasttower.conf import settings
    for app in settings.INSTALLED_APPS:
        try:
            import_module(f'{app}.admin')
        except ModuleNotFoundError:
            pass


__all__ = [
    'timezone',
    'lifespans',
    'get_module',
    'register_orm',
    'get_user_model',
    'setup',
]
