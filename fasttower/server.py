from typing import Annotated, Optional, Sequence, Any, TypeVar

from fastapi import FastAPI
from fasttower.conf import settings
from fasttower.utils import get_module
from starlette.middleware import Middleware
from typing_extensions import Doc

AppType = TypeVar("AppType", bound="FastTower")


class FastTower(FastAPI):
    """
    `FastTower` app class, the main entrypoint to use FastTower.

    ## Example

    ```python
    from fasttower.server import FastTower

    app = FastTower()
    ```
    """

    def __init__(self: AppType, *,
                 debug: Annotated[
                     bool,
                     Doc(
                         """
                         Boolean indicating if debug tracebacks should be returned on server
                         errors.

                         Read more in the
                         [Starlette docs for Applications](https://www.starlette.io/applications/#instantiating-the-application).
                         """
                     ),
                 ] = None,
                 middleware: Annotated[
                     Optional[Sequence[Middleware]],
                     Doc(
                         """
                         List of middleware to be added when creating the application.

                         In FastTower you would normally do this with `app.add_middleware()`
                         instead.

                         Read more in the
                         [FastAPI docs for Middleware](https://fastapi.tiangolo.com/tutorial/middleware/).
                         """
                     ),
                 ] = None,
                 **extra: Annotated[
                     Any,
                     Doc(
                         """
                         Extra keyword arguments to be stored in the app, not used by FastTower.
                         anywhere.
                         """
                     ),
                 ], ):
        if debug is None:
            debug = settings.DEBUG or False
        if middleware is None:
            middleware = settings.MIDDLEWARE
        super().__init__(debug=debug, **extra)

        for middleware_ in middleware:
            self.add_middleware(get_module(middleware_[0]), **middleware_[1] if len(middleware_) > 1 else {})
