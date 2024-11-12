# Приступаем

После установки зависимостей давайте приступим к созданию первого приложения! Многие вещи вам уже знакомы из опыта с
FastAPI

!!! example "Полный пример"

    Пример содержит отправку писем по SMTP, кэширование, добавление новых команд, tortoise-orm, lifespans 
    [example](https://github.com/pysashapy/fasttower/tree/main/examples/maximun_example)

## Создание проекта

Для начала создайте проект командой:

```bash
tower g p example
```

После выполнения команды, вы можете обнаружить Django-like структуру проекта и сразу же запустить сервер!

=== "fasttower manage.py"

    ```bash
    python manage.py run
    ```

=== "fasttower tower"

    ```bash
    tower run
    ```
    !!! note
        Перед испольвазнием **tower** для запуска сервера, работы с бд и т.д. Убедитесь что установлена переменная окружения FASTTOWER_SETTINGS_MODULE

=== "uvicorn"

    ```bash
    uvicorn example.asgi:app 
    ```

=== "hypercorn"

    ```bash
    hypercorn example.asgi:app 
    ```

Вот и все, вы построили первое работающее веб приложение!
Но давайте разберемся что из себя представляет сгенерированный проект и напишем новый функционал помимо работающего
Swagger-a из коробки.

## Структура

После создания проекта командой:

```bash
tower g p example
```

Вы должны увидеть следующею структуру:

```text
├── example/
│   ├── __init__.py
│   ├── asgi.py
│   ├── routers.py
│   └── settings.py
└── manage.py
```

Далее мы выясним, что в них находится!

### manage.py

Служит для установки переменной **FASTTOWER_SETTINGS_MODULE** задающей путь до файла settings.py после чего запускает
cli.
Вы можете установить данную переменную в окружение и забыть о **python manage.py** вызывая cli **tower** командой

=== "manage"

    ```bash
    python manage.py --help
    ```

=== "tower"

    ```bash
    tower --help
    ```

???+ note "manage.py"

    ```python 
    #!/usr/bin/env python
    """FastTower's command-line utility for administrative tasks."""
    import os
    
    
    def main():
        """Run administrative tasks."""
        os.environ.setdefault("FASTTOWER_SETTINGS_MODULE", "example.settings")
        try:
            from fasttower.cli import app
            app()
        except ImportError as exc:
            raise ImportError(
                "Couldn't import FastTower. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
    
    
    if __name__ == '__main__':
        main()
    ```

### settings.py

В нем можно добавлять новые middleware - которые автоматически привяжутся к экземпляру FastTower, регистрировать app,
так же задавать часовой пояс, secret key, debug режим и прочее.

???+ note "settings.py"

    ```python 
    from pathlib import Path
    
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = "l6q4CY6UhJXppm8TjiyhUF2nhEGaX1aPao3RnkyRavY"
    
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    
    ALLOWED_HOSTS = ["*"]
    
    INSTALLED_APPS = [
        'fasttower.apps.taerich',
        'fasttower.auth',
    ]
    
    MIDDLEWARE = [
        ["fastapi.middleware.trustedhost.TrustedHostMiddleware", {"allowed_hosts": ALLOWED_HOSTS}],
        ["fastapi.middleware.gzip.GZipMiddleware", {"minimum_size": 1000, "compresslevel": 5}],
    ]
    if DEBUG:
        MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"],
    
    USER_MODEL = 'fasttower.auth.models.BaseUser'
    
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
    
    CACHE = {
        "default": {
            "BACKEND": "fasttower.cache.InMemoryBackend",
        }
    }
    
    #https://github.com/fastapi-admin/fastapi-admin
    ADMIN_PANEL_REDIS = 'redis://localhost:6379/0'
    ```

### asgi.py

FastTower унаследован от FastAPI и выполняет роль для установки middleware, debug режима. Вы можете переназначить
значения, которые выставляются из settings.py:

```python
app = FastTower(debug=True, title="FastTower API Documentation",
                lifespan=lifespans([tortoise_lifespan, cache_lifespan]))
```

В этом примере даже если в settings установлен DEBUG=False, окончательно будет установлен True

Если вы не используете tortoise или cache - уберите их из lifespans

```python
app = FastTower(title="FastTower API Documentation", lifespan=lifespans([]))
```

???+ note "asgi.py"

    ```python 
    """
    ASGI config for example project.
    
    It exposes the ASGI callable as a module-level variable named ``app``.
    """
    
    import os
    
    from fasttower.utils import setup
    
    os.environ.setdefault("FASTTOWER_SETTINGS_MODULE", "example.settings")
    setup()
    
    from fasttower.server import FastTower
    
    from fasttower.utils import lifespans
    from fasttower.cache.lifespan import cache_lifespan
    from fasttower.db.lifespan import tortoise_lifespan
    
    from example.routers import router
    
    app = FastTower(title="FastTower API Documentation", lifespan=lifespans([tortoise_lifespan, cache_lifespan]))
    
    app.include_router(router)
    ```

### routers.py

[О APIRouter](https://fastapi.tiangolo.com/reference/apirouter/)

???+ note "routers.py"

    ```python
    from fasttower.routers import APIRouter
    
    from appexample.routers import router as appexample_router
    
    router = APIRouter(prefix="/api/v1")
    router.include_router(appexample_router)
    
    ```
