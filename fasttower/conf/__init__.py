import importlib
import os
import sys
from pathlib import Path

from fasttower.apps.config import AppBaseConfig

FASTTOWER_SETTINGS_MODULE = "FASTTOWER_SETTINGS_MODULE"


class TypedSettings:
    DEBUG: bool
    SECRET_KEY: str
    BASE_DIR: Path
    ALLOWED_HOSTS: list[str]
    INSTALLED_APPS: list[str]
    MIDDLEWARE: list[list[str, dict]]
    USER_MODEL: str
    ASGI: str
    LANGUAGE_CODE: str
    TIME_ZONE: str
    USE_TZ: bool
    DATABASES: dict
    COMMANDS: list


class Settings(TypedSettings):

    def __init__(self):
        try:
            settings_module = os.environ.get(FASTTOWER_SETTINGS_MODULE)
            if not settings_module:
                raise EnvironmentError(
                    f"Environment variable {FASTTOWER_SETTINGS_MODULE} is not defined."
                )

            current_dir = os.getcwd()
            if current_dir not in sys.path:
                sys.path.append(current_dir)

            self._settings = importlib.import_module(settings_module)

            def read_config(config: AppBaseConfig):
                config.read()

            def extend_commands(config: AppBaseConfig):
                self._settings.COMMANDS.extend(config.typer_apps)

            def extend_databases(config: AppBaseConfig):
                db_apps: dict = self._settings.DATABASES.setdefault('apps', {})
                models: list[str] = db_apps.setdefault(config.app, {
                    "models": [],
                    "default_connection": config.db,
                })['models']
                models.append(config.models_location)

            setattr(self._settings, 'COMMANDS', [])
            self._settings.DATABASES.setdefault("use_tz", self._settings.USE_TZ)
            self._settings.DATABASES.setdefault("timezone", self._settings.TIME_ZONE)

            for app in getattr(self._settings, 'INSTALLED_APPS', []):
                config_ = importlib.import_module(f"{app}.config").AppConfig()
                extend_databases(config_)
                extend_commands(config_)

                read_config(config_)

            for attr in dir(self._settings):
                if attr == attr.upper():
                    value = getattr(self._settings, attr)
                    setattr(self, attr, value)

        except Exception as e:
            raise ImportError(
                f"Settings cannot be loaded"
            ) from e


settings = Settings()
