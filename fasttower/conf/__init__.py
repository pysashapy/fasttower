import importlib
import os
import sys

from fasttower.apps.config import AppBaseConfig

FASTTOWER_SETTINGS_MODULE = "FASTTOWER_SETTINGS_MODULE"


class Settings:

    def __init__(self):
        try:
            settings_module = os.environ.get(FASTTOWER_SETTINGS_MODULE)
            current_dir = os.getcwd()
            if current_dir not in sys.path:
                sys.path.append(current_dir)
            self.settings = importlib.import_module(settings_module)
        except Exception:
            self.settings = {}
            return
        self.extend_settings()

    def extend_settings(self):
        setattr(self.settings, 'COMMANDS', [])
        for app in self.get_installed_apps():
            config = importlib.import_module(f"{app}.config").AppConfig()
            self.extend_databases(config)
            self.extend_commands(config)

            self.read_config(config)

    def read_config(self, config: AppBaseConfig):
        config.read()

    def extend_commands(self, config: AppBaseConfig):
        self.settings.COMMANDS.extend(config.typer_apps)

    def extend_databases(self, config: AppBaseConfig):
        self.settings.DATABASES.setdefault("use_tz", self.settings.USE_TZ)
        self.settings.DATABASES.setdefault("timezone", self.settings.TIME_ZONE)

        db_apps: dict = self.settings.DATABASES.setdefault('apps', {})
        models: list[str] = db_apps.setdefault(config.app, {
            "models": [],
            "default_connection": config.db,
        })['models']
        models.append(config.models_location)

    def get_installed_apps(self):
        return getattr(self.settings, 'INSTALLED_APPS', [])


settings = Settings().settings
