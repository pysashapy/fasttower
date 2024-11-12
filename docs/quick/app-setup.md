# Новое приложение

После разбора структуры проекта давайте добавим новое app которое будет отвечать за отправку email сообщений и получения
кэшированной истории сообщений!
А добавить его очень легко, просто выполните команду:

=== "manage"

    ```bash
    python manage.py g a emailapp
    ```

=== "tower"

    ```bash
    tower g a emailapp
    ```
    !!! note
        Перед испольвазнием **tower** для запуска сервера, работы с бд и т.д. Убедитесь что установлена переменная окружения FASTTOWER_SETTINGS_MODULE

У вас будет следующая структура проекта:

```text
├── emailapp/
│   ├── __init__.py
│   ├── admin.py
│   ├── config.py
│   ├── models.py
│   ├── routers.py
│   ├── serializers.py
│   └── views.py
├── example/
│   ├── __init__.py
│   ├── asgi.py
│   ├── routers.py
│   └── settings.py
└── manage.py
```

!!! warning "Подключение приложения"

    Таких приложений может быть много и важно все приложения которые используются вносить в INSTALLED_APPS

    ```python
    INSTALLED_APPS = [
        'fasttower.apps.taerich',
        'fasttower.auth',
        ...,
        'emailapp',
    ]
    ```

??? note "settings.py"

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
        'emailapp',
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

## Структура приложения

### config.py

Отвечает за инициализацию моделей, cli команд

!!! note "config.py"

    ```python
    from fasttower.apps.config import AppBaseConfig


    class AppConfig(AppBaseConfig):
        app = 'emailapp'
    ```

Если вам требуется инициализировать что-либо при запуске проекта, внесите это в функцию read

```python
from fasttower.apps.config import AppBaseConfig


class AppConfig(AppBaseConfig):
    app = 'emailapp'

    def read(self):
        ...
```

### models.py

!!! warning "ORM"

    В настоящее время из коробки поддерживаться только Tortoise-orm

!!! note "models.py"

    ```python
    from fasttower.db import models
    ```

В настоящее время models.Model реализует только primary key

```python
class Model(tortoise.Model):
    id: int = tortoise.fields.IntField(pk=True)

    class Meta:
        abstract = True
```

!!! note "Пример модели"

    ```python
    from email.message import EmailMessage
    
    from fasttower.conf import settings
    from fasttower.db import models
    from fasttower.email import send_mail
    
    
    class EmailMessageModel(models.Model):
        subject = models.CharField(max_length=100)
        content = models.TextField()
        to = models.CharField(max_length=255)
        create_at = models.DatetimeField(auto_now_add=True, null=True, default=None)
    
        async def send(self):
            message = EmailMessage()
            message["From"] = settings.SMTP['default']['from_']
            message["To"] = self.to
            message["Subject"] = self.subject
            message.set_content(self.content)
            await send_mail(message=message)
    ```

Документация Tortoise <https://tortoise.github.io/>

### admin.py

!!! warning "Admin panel"

    В настоящее время совместимо только с Tortoise-orm

Вы должны увидеть следующее содержимой, а так же просмотреть документацию можно
тут <https://fastapi-admin-docs.long2ice.io/>

!!! note "admin.py"

    ```python
    from fastapi_admin.resources import Model, Dropdown
    from fasttower import admin
    
    from emailapp import models
    
    
    @admin.site.app.register
    class EmailappTabMenu(Dropdown):
        label = "emailapps"
        icon = "fas fa-bars"
        resources = []
        title = "Emailapps"
     ```

## Создаем модель

После того как вы разобрались со структурой приложений, давай те сделаем первую модель которая будет хранить
subject,content,to,create_at. Для этого создайте класс унаследованный от models.Model

```python
class EmailMessageModel(models.Model):
```

И добавьте новые поля

```python
subject = models.CharField(max_length=100)
content = models.TextField()
to = models.CharField(max_length=255)
create_at = models.DatetimeField(auto_now_add=True, null=True, default=None)
```

!!! note "Полный код"

    ```python
    from email.message import EmailMessage

    from fasttower.conf import settings
    from fasttower.db import models
    from fasttower.email import send_mail
    
    
    class EmailMessageModel(models.Model):
        subject = models.CharField(max_length=100)
        content = models.TextField()
        to = models.CharField(max_length=255)
        create_at = models.DatetimeField(auto_now_add=True, null=True, default=None)

    async def send(self):
        message = EmailMessage()
        message["From"] = settings.SMTP['default']['from_']
        message["To"] = self.to
        message["Subject"] = self.subject
        message.set_content(self.content)
        await send_mail(message=message)
    ```

## Конечные точки

в файле views.py, задайте две конечные точки:

!!! note "Полный код"

    ```python
    from emailapp.models import EmailMessageModel
    from pydantic import EmailStr
    
    from fasttower.cache import cache
    from fasttower.routers import APIRouter
    
    router = APIRouter()
    
    
    @router.get("/send")
    async def send_message(subject: str, content: str, to: EmailStr):
        message = EmailMessageModel(subject=subject, content=content, to=to)
        await message.save()
        await message.send()
    
    
    @router.get("/history")
    @cache(expire=1)
    async def message_history():
        return await EmailMessageModel.all()
    
    ```

Использую следующий декоратор, вы задаете время кэширования в минутах

```python
@cache(expire=1)
```

!!! warning "Убедитесь в уставленном lifespan для кэша **cache_lifespan**"

    ```python
        app = FastTower(title="FastTower API Documentation", lifespan=lifespans([cache_lifespan]))
    ```

!!! note

    Подключите router к главному роутеру в example/routers.py

    !!! note "emailapp/routers.py"
    
        ```python
        from fasttower.routers import APIRouter
        
        from emailapp.views import router as email_router
        
        router = APIRouter(prefix="/emailapp", tags=["emailapp"])
        router.include_router(email_router)
        ```
    
    !!! note "example/routers.py"
    
        ```python
        from fasttower.routers import APIRouter
        
        from emailapp.views import router as email_router
        
        router = APIRouter(prefix="/emailapp", tags=["emailapp"])
        router.include_router(email_router)
        ```

## Подключаем SMTP

В файле settings.py установите следующую настройку

```python
SMTP = {
    'default': {
        'backend': 'fasttower.email.backends.AIOEmailBackend',
        'hostname': 'smtp.example.org',
        'port': 465,
        'username': 'example',
        'password': 'example',
        'use_tls': True,
        'start_tls': False,
        'from_': 'example@example.org'
    }
}
```

## Миграции

Мы подошли к концу, давайте создадим миграции и запустим приложение

!!! note "Миграции"

    === "manage"

        ```bash
        python manage.py db init
        ```

    === "tower"
    
        ```bash
        tower db init
        ```
        !!! note
            Перед испольвазнием **tower** для запуска сервера, работы с бд и т.д. Убедитесь что установлена переменная окружения FASTTOWER_SETTINGS_MODULE

После успешного создания миграций, в корне проекта вы обнаружите соответствующую папку и sql для обновления бд

!!! note "Запуск"

    === "manage"

        ```bash
        python manage.py run
        ```

    === "tower"
    
        ```bash
        tower run
        ```
        !!! note
            Перед испольвазнием **tower** для запуска сервера, работы с бд и т.д. Убедитесь что установлена переменная окружения FASTTOWER_SETTINGS_MODULE

На этом все, вы можете перейти в свагер и отправить письмо, а так же получить всю историю писем!
