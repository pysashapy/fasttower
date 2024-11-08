import uuid

import redis.asyncio as redis
from fastapi import Depends
from fastapi_admin import constants
from fastapi_admin.depends import get_redis
from fastapi_admin.i18n import _
from fastapi_admin.models import AbstractAdmin
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin.template import templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_401_UNAUTHORIZED
from fasttower.auth.models import AnonymousUser


class AdminUserProvider(UsernamePasswordProvider):
    async def get_admin(self, request: Request, username: str, password: str):
        admin = await self.admin_model.get_or_none(username=username)
        if not admin or not admin.check_password(password) or not admin.is_superuser:
            return AnonymousUser()
        return admin

    async def login(self, request: Request, redis: redis.Redis = Depends(get_redis)):
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        remember_me = form.get("remember_me")
        admin = await self.get_admin(request, username, password)

        if getattr(admin, "is_anonymous", True):
            return templates.TemplateResponse(
                self.template,
                status_code=HTTP_401_UNAUTHORIZED,
                context={"request": request, "error": _("login_failed")},
            )

        response = RedirectResponse(url=request.app.admin_path, status_code=HTTP_303_SEE_OTHER)
        if remember_me == "on":
            expire = 3600 * 24 * 30
            response.set_cookie("remember_me", "on")
        else:
            expire = 3600
            response.delete_cookie("remember_me")
        token = uuid.uuid4().hex
        response.set_cookie(
            self.access_token,
            token,
            expires=expire,
            path=request.app.admin_path,
            httponly=True,
        )
        await redis.set(constants.LOGIN_USER.format(token=token), admin.pk, ex=expire)
        return response

    async def pre_save_admin(self, _, instance: AbstractAdmin, using_db, update_fields):
        pass

    async def create_user(self, username: str, password: str, **kwargs):
        admin = self.admin_model(username=username, is_staff=True)
        admin.password = password
        await admin.save()
        return admin


def admin_provider(**kwargs):
    from fasttower.utils import get_user_model

    return AdminUserProvider(
        admin_model=get_user_model(),
        login_logo_url="https://preview.tabler.io/static/logo.svg",
        **kwargs
    )
