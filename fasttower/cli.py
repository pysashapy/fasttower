# cli.py
import asyncio

import typer
from fasttower.blueprints.commands import blueprints_commands
from fasttower.conf import settings
from fasttower.db.commands import db_commands

app = typer.Typer()

for typer_app in getattr(settings, 'COMMANDS', []) + [
    db_commands,
    blueprints_commands
]:
    app.add_typer(typer_app)


@app.command()
def run():
    """Запуск FastTower сервера"""
    import uvicorn
    uvicorn.run(settings.ASGI, host='127.0.0.1', port=8000, reload=True)


@app.command()
def shell():
    """Запускает интерактивную оболочку."""
    import IPython
    from fasttower.utils import setup
    setup()
    ipython = IPython.terminal.embed.InteractiveShellEmbed()
    ipython()


async def create_superuser(username, password):
    from fasttower.db import initialize_tortoise
    from fasttower.utils import get_user_model
    from tortoise import Tortoise
    await initialize_tortoise()
    try:
        user_model = get_user_model()

        user_exists = await user_model.filter(username=username).exists()
        if user_exists:
            typer.echo(f"Username '{username}' already exists. Please choose a different username.")
            raise typer.Exit(code=1)

        user = user_model(username=username, is_staff=True)
        user.password = password
        await user.save()
    finally:
        await Tortoise.close_connections()


@app.command("superuser", help="Create a superuser.")
def addsuperuser():
    username = typer.prompt("Enter a username")
    password = typer.prompt("Enter a password", hide_input=True)
    confirm_password = typer.prompt("Confirm password", hide_input=True)

    if password != confirm_password:
        typer.echo("Passwords do not match. Please try again.")
        raise typer.Exit(code=1)

    asyncio.run(create_superuser(username, password))

    typer.echo(f"Superuser '{username}' created successfully.")


if __name__ == "__main__":
    app()
