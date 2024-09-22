import redis.asyncio as redis
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi_admin.app import app
from fastapi_admin.depends import get_resources
from fastapi_admin.exceptions import unauthorized_error_exception, forbidden_error_exception, not_found_error_exception, \
    server_error_exception
from fastapi_admin.template import add_template_folder, templates
from fasttower import admin
from fasttower.auth.providers import admin_provider
from pathlib import Path
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, \
    HTTP_401_UNAUTHORIZED

BASE_DIR = Path(__file__).resolve().parent
add_template_folder(BASE_DIR / 'templates')

app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)
app.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)
app.add_exception_handler(HTTP_401_UNAUTHORIZED, unauthorized_error_exception)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@asynccontextmanager
async def lifespan_admin(app: FastAPI):
    r = redis.from_url(
        "redis://localhost",
        decode_responses=True,
        encoding="utf8",
    )
    await admin.site.app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        favicon_url="https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/favicon.png",
        providers=[
            admin_provider()
        ],
        redis=r,
    )
    yield


@app.get("/")
async def home(
        request: Request,
        resources=Depends(get_resources),
):
    return templates.TemplateResponse(
        "dashboard.html",
        context={
            "title": 'FastTower | Admin',
            "request": request,
            "resources": resources,
        },
    )
