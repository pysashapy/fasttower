DEBUG = False

ALLOWED_HOSTS = []
INSTALLED_APPS = []
MIDDLEWARE = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_TZ = True

CACHE = {
    "default": {
        "BACKEND": "fasttower.cache.InMemoryBackend",
    }
}
