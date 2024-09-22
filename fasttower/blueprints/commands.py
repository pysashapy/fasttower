import os
import secrets
import typer
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

blueprints_commands = typer.Typer(name='g', help='Generate project structures and app components for FastTower.')
BASE_DIR = Path(__file__).resolve().parent


@blueprints_commands.command()
def p(project_name: str) -> None:
    """
    Generate a new FastTower project with the specified structure.

    :param project_name: The name of the new project.
    :type project_name: str
    :return: None
    """
    env = Environment(loader=FileSystemLoader(BASE_DIR / 'templates' / 'project'))

    project_path = os.path.join(project_name)
    os.makedirs(project_path, exist_ok=True)

    secret_key = secrets.token_urlsafe(32)

    # Define templates and their corresponding filenames
    templates = {
        "manage.py.jinja": "manage.py",
        "project_name/__init__.py.jinja": os.path.join(project_path, "__init__.py"),
        "project_name/settings.py.jinja": os.path.join(project_path, "settings.py"),
        "project_name/asgi.py.jinja": os.path.join(project_path, "asgi.py"),
        "project_name/routers.py.jinja": os.path.join(project_path, "routers.py"),
    }

    # Generate files from templates
    for template_name, output_name in templates.items():
        template = env.get_template(template_name)
        with open(output_name, 'w') as f:
            f.write(template.render(project_name=project_name, secret_key=secret_key))

    typer.echo(f"Project '{project_name}' created successfully!")


@blueprints_commands.command()
def a(app_name: str) -> None:
    """
    Generate a new FastTower application with the specified structure.

    :param app_name: The name of the new application.
    :type app_name: str
    """

    env = Environment(loader=FileSystemLoader(BASE_DIR / 'templates' / 'app'))

    app_path = os.path.join(app_name)
    os.makedirs(app_path, exist_ok=True)

    templates = {
        "__init__.py.jinja": os.path.join(app_path, "__init__.py"),
        "config.py.jinja": os.path.join(app_path, "config.py"),
        "admin.py.jinja": os.path.join(app_path, "admin.py"),
        "models.py.jinja": os.path.join(app_path, "models.py"),
        "routers.py.jinja": os.path.join(app_path, "routers.py"),
        "serializer.py.jinja": os.path.join(app_path, "serializer.py"),
        "views.py.jinja": os.path.join(app_path, "views.py"),
    }

    for template_name, output_name in templates.items():
        template = env.get_template(template_name)
        with open(output_name, 'w') as f:
            f.write(template.render(app_name=app_name))
    typer.echo(f"Application '{app_name}' created successfully!")


if __name__ == "__main__":
    blueprints_commands()
