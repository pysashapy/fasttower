from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "niJEjVCDfqHI_Fke_oUDVgcqkfWfW8ZEoUT_OQxVKco"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'fasttower.apps.taerich',
    'fasttower.auth',
    'appexample',
]

MIDDLEWARE = [
    ["fastapi.middleware.trustedhost:TrustedHostMiddleware", {"allowed_hosts": ALLOWED_HOSTS}],
    ["fastapi.middleware.gzip:GZipMiddleware", {"minimum_size": 1000, "compresslevel": 5}],
]
if DEBUG:
    MIDDLEWARE += ["debug_toolbar.middleware:DebugToolbarMiddleware"],

USER_MODEL = 'fasttower.auth.models:BaseUser'

ASGI = "example.asgi:app"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_TZ = True

# Database
DATABASES = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {
                "file_path": str(BASE_DIR / "db.sqlite3"),
            }
        },
    },
}

# https://github.com/fastapi-admin/fastapi-admin
ADMIN_PANEL_REDIS = 'redis://localhost:6379/0'
