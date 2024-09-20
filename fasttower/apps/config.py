
import importlib

import typer


class AppBaseConfig:
    app = None  # The name of the app relative to the manage.py file.

    db = 'default'  # The default database connection name.
    models = 'models'  # The name of the module containing the app's models.

    commands = 'commands'  # The module where Typer commands for the app are implemented.

    def __init__(self):
        if self.app is None:
            raise ValueError("Attribute 'app' must be set in the subclass of AppConfig.")

    def read(self):
        """Placeholder method for user-defined configuration logic."""
        pass

    @property
    def models_location(self):
        """Returns the fully qualified path to the app's models module."""
        return f"{self.app}.{self.models}"

    @property
    def typer_apps(self):
        """Imports and returns a list of Typer commands defined in the commands module."""
        try:
            commands_module = importlib.import_module(f"{self.app}.{self.commands}")
        except ModuleNotFoundError:
            return []

        commands = []
        for obj_name in dir(commands_module):
            obj = getattr(commands_module, obj_name)
            if isinstance(obj, typer.main.Typer):
                commands.append(obj)
        return commands
