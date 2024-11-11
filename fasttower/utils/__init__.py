from contextlib import asynccontextmanager, AsyncExitStack
from importlib import import_module
from typing import List, Callable

from fastapi import FastAPI
from tortoise import timezone


def get_class(path: str, seps=':.'):
    try:
        for sep in seps:
            path_ = path.rsplit(sep, maxsplit=1)
            if len(path_) == 2:
                path, class_ = path_
                break
        else:
            raise ValueError
        return getattr(import_module(path), class_)
    except (ModuleNotFoundError, ValueError):
        raise ImportError(f'class <{path}> not be imported')


def get_user_model():
    from fasttower.conf import settings
    return get_class(settings.USER_MODEL)


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
    'get_user_model',
    'setup',
    'get_class'
]
