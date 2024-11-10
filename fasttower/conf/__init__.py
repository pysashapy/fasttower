import importlib
import logging
import os
import sys
from pathlib import Path
from fasttower.conf import global_settings
FASTTOWER_SETTINGS_MODULE = "FASTTOWER_SETTINGS_MODULE"


class SettingsTyped:
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


class Settings(SettingsTyped):

    def __init__(self):
        self.configure(global_settings)

        try:
            settings_module = os.environ.get(FASTTOWER_SETTINGS_MODULE)
            if not settings_module:
                logging.warning(
                    f"Environment variable {FASTTOWER_SETTINGS_MODULE} is not defined."
                )
                return

            current_dir = os.getcwd()
            if current_dir not in sys.path:
                sys.path.append(current_dir)

            self._settings = importlib.import_module(settings_module)

            setattr(self._settings, 'COMMANDS', [])
            self._settings.DATABASES.setdefault("use_tz", self._settings.USE_TZ)
            self._settings.DATABASES.setdefault("timezone", self._settings.TIME_ZONE)

            for app in getattr(self._settings, 'INSTALLED_APPS', []):
                config_ = importlib.import_module(f"{app}.config").AppConfig()

                db_apps: dict = self._settings.DATABASES.setdefault('apps', {})
                models: list[str] = db_apps.setdefault(config_.app, {
                    "models": [],
                    "default_connection": config_.db,
                })['models']
                models.append(config_.models_location)

                self._settings.COMMANDS.extend(config_.typer_apps)
                config_.read()

            self.configure(self._settings)

        except Exception:
            logging.warning(
                f"Settings cannot be loaded"
            )

    def configure(self, module):
        for attr in dir(module):
            if attr == attr.upper():
                value = getattr(module, attr)
                setattr(self, attr, value)


try:
    settings = Settings()
except (ImportError, EnvironmentError):
    logging.exception("Settings cannot be loaded")
    settings = object
