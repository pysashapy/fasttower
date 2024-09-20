# cli.py
import subprocess
import typer

from fasttower.conf import settings
from fasttower.db.commands import db_commands
from fasttower.blueprints.commands import blueprints_commands

app = typer.Typer()

for typer_app in settings.COMMANDS + [
    db_commands,
    blueprints_commands
]:
    app.add_typer(typer_app)


@app.command()
def run():
    """Запуск FastTower сервера"""
    import uvicorn
    uvicorn.run(settings.ASGI, host='127.0.0.1', port=8000, reload=True)


if __name__ == "__main__":
    app()
