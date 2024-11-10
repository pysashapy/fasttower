<h1 align="center">FastTower</h1>
<p align="center">
    <em>FastTower — это молодой фреймворк основанный на FastAPI для быстрого создания серверных приложений с Django-like структурой.</em>
</p>
<p align="center">
<a href="https://pypi.org/project/fasttower" target="_blank">
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/fasttower">
</a>
<a href="https://pypi.org/project/fasttower" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fasttower.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

# Features

- Легкая настройка
- Высокая производительность
- Простота в использовании
- Админ панель

# Быстрый старт

В настоящее время официально поддерживаться только tortoise orm и админ панель для нее, но вы можете легко добавить свою
поддержку бд модернизируя
FastTower app в asgi.py файле

<details markdown="1">
<summary>Полный пример...</summary>
на [github](https://github.com/pysashapy/fasttower/tree/main/examples/start)
</details>

## Установка

```bash
pip install fasttower[tortoise]
```

Так же для управления миграциями требуется aerich, а именно его модернизированный форк

```bash
pip install git+https://github.com/pysashapy/taerich.git@0.0.1
```

## Создание проекта

Для начала требуется сгенерировать основное приложение

```bash
tower g p example
```

После выполнения команды, вы можете обнаружить Django-like структуру проекта и сразу же запустить сервер

```bash
python manage.py run
```

<details markdown="1">
<summary>Или другим сервером...</summary>
```bash
uvicorn example.asgi:app 
```
</details>

## Обзор

Главная роль manage.py файла установить env **FASTTOWER_SETTINGS_MODULE** указывающею путь до вашего settings.py файла(*
*example.settings**). Вы можете
установить ее сами и после этого использовать команду **tower**. Далее будет использоваться команда **tower**, но вы
всегда можете использовать **python manage.py**
<details markdown="1">
<summary>Запуск с установленной env...</summary>
```bash
tower run
```
</details>

## Структура проекта

### asgi.py

FastTower - это полностью совместимый FastAPI class.

```python
"""
ASGI config for example project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

from fasttower.utils import setup

os.environ.setdefault("FASTTOWER_SETTINGS_MODULE", "example.settings")
setup()

from fasttower.server import FastTower

from example.routers import router

app = FastTower(title="FastTower API Documentation")

app.include_router(router)
```

<details markdown="1">
<summary>Если не нужен tortoise...</summary>
Уберите lifespan
```python
lifespan=lifespans([tortoise_lifespan])
```
</details>

### settings.py

Вправду очень похоже на Django?

Основные поля: INSTALLED_APPS, MIDDLEWARE, USER_MODEL(Только tortoise!)

```python
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
```

#### INSTALLED_APPS

После создания нового приложения обязательно добавьте его в **INSTALLED_APPS**! Иначе у FastTower не будет доступа к
моделям и командам
приложения

#### MIDDLEWARE

Поддерживаются все starlette совместимые middleware!

Структура MIDDLEWARE

```python
MIDDLEWARE = [
    ["fastapi.middleware.trustedhost:TrustedHostMiddleware", {"allowed_hosts": ALLOWED_HOSTS}],
    ["fastapi.middleware.gzip:GZipMiddleware", {"minimum_size": 1000, "compresslevel": 5}],
    ...
    ["path:class", {...kwargs}],
]
```

### routers.py

Является отправной точкой для всех будущих APPs

```python
from fasttower.routers import APIRouter

router = APIRouter(prefix="/api/v1")
router.include_router(APP_ROUTER, prefix='/app')
```

## Создание нового приложения

Выполните команду которая создаст приложение

```bash 
tower g a appexample
```

После ее выполнения обязательно добавьте приложение в **settings.py -> INSTALLED_APPS**

```python
INSTALLED_APPS = [
    'fasttower.apps.taerich',
    'fasttower.auth',
    ...
    'appexample',
]
```

Каждое приложение содержит **config.py, models.py, admin.py, serializers.py, routers.py и views.py**

### Models

Основано на [tortoise](https://tortoise.github.io/), так что вы можете просто импортировать ее и работать с ней!

```python
from fasttower.db import models


class FastTowerModel(models.Model):
    say = models.CharField(max_length=100, default="Hello World!")
```

### Admin

Тут содержится описание моделей для [админ панели](https://fastapi-admin-docs.long2ice.io/)

```python
from fastapi_admin.resources import Model, Dropdown
from fasttower import admin

from appexample import models


@admin.site.app.register
class AppexampleTabMenu(Dropdown):
    label = "Appexamples"
    icon = "fas fa-bars"
    resources = []
    title = "Appexamples"
```

### Views

Тут все аналогично FastAPI, скоро появятся **mixins** как в Django для простых **CRUD** задач!

```python
from appexample.models import FastTowerModel

from fasttower.routers import APIRouter

router = APIRouter()


@router.get("/")
async def say():
    return await FastTowerModel().create()
```

Не забудьте подключить в **appexample.routers**, а так же в **example.routers**

## Admin panel

Является экспериментальной функцией. В настоящее время для ее работы требуется
[**Redis**](https://github.com/redis/redis-py)

Проверьте в settings.py

```
ADMIN_PANEL_REDIS = 'redis://localhost:6379/0'
```

А так же включите его в asgi.py

```python
from fasttower.admin.site import app as admin_app, lifespan_admin
from fasttower.db import lifespan

app = FastTower(title="FastTower API Documentation", lifespan=lifespans([lifespan, lifespan_admin]))

app.mount('/admin', admin_app)

```

<details markdown="1">
<summary>Полный код...</summary>
```python
"""
ASGI config for example project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

from fasttower.utils import setup, lifespans

os.environ.setdefault("FASTTOWER_SETTINGS_MODULE", "example.settings")
setup()

from fasttower.server import FastTower

from example.routers import router
from fasttower.admin.site import app as admin_app, lifespan_admin
from fasttower.db import lifespan

app = FastTower(title="FastTower API Documentation", lifespan=lifespans([lifespan, lifespan_admin]))

app.mount('/admin', admin_app)

app.include_router(router)

```
</details>

## Commands
Список текущих команд и их описания вы можете получить используя команду
```bash
tower --help
```

```text
 Usage: tower [OPTIONS] COMMAND [ARGS]...                                                                                                                                                                                         

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                                                                        │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                                                                                 │
│ --help                        Show this message and exit.                                                                                                                                                                      │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ db          Database commands                                                                                                                                                                                                  │
│ g           Generate project structures and app components for FastTower.                                                                                                                                                      │
│ run         Запуск FastTower сервера                                                                                                                                                                                           │
│ shell       Запускает интерактивную оболочку.                                                                                                                                                                                  │
│ superuser   Create a superuser.                                                                                                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Создание новых команд

Для этого создайте файл в папке **app**(appexample) commands.py

```python
import typer

example_commands = typer.Typer(name="appexample", help="Example commands")


@example_commands.command()
def hello_world():
    print("Hello World!")

```

Вот и все её можно запустить!

```bash
tower appexample hello-world
```

```bash
Hello World!
```

Более детально про [Typer](https://typer.tiangolo.com/)

# Продолжение следует...