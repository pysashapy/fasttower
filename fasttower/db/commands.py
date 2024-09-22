import asyncio
from typing import Annotated, Optional

import typer
from aerich import Command
from tortoise import Tortoise

from fasttower.conf import settings
from fasttower.db import initialize_tortoise

db_commands = typer.Typer(name="db", help="Database commands")


async def run_aerich_command(action: str, app_name: Optional[str] = None,
                             safe: bool = True, transaction: bool = True) -> None:
    """
    Execute Aerich commands for the specified action on the registered application.

    :param action: The action to perform. Possible values are:
        - "initialization": Initialize the database for the application.
        - "create migrations": Create migrations for the application.
        - "apply migrations": Apply migrations for the application.
    :param app_name: The specific application to target.
                     If None, applies to all registered applications.
    :param safe: If True, perform safe operations that won't result in data loss.
                    Default is True.
    :param transaction: If True, run the operation within a transaction.
                               Default is True.
    """
    try:
        await initialize_tortoise()
        apps = [app_name] if app_name is not None else settings.DATABASES['apps'].keys()
        for app in apps:
            try:
                typer.echo(f"🔄 {action.capitalize()} for application: {app}")
                aerich_command = Command(tortoise_config=settings.DATABASES, app=app)
                await aerich_command.init()
                if action == "initialization":
                    await aerich_command.init_db(safe)
                elif action == "create migrations":
                    await aerich_command.migrate(app)
                elif action == "apply migrations":
                    await aerich_command.upgrade(transaction)
            except Exception as e:
                raise e
                typer.echo(f"❌ Error in application '{app}': {str(e)}", err=True)
                continue
    finally:
        await Tortoise.close_connections()


@db_commands.command()
def init(
        safe: bool = typer.Option(
            True, help="If True, perform safe operations that won't result in data loss."
        ),
) -> None:
    """
    Initialize the database for all applications by running the appropriate Aerich command.

    :param safe: If True, perform safe operations that won't result in data loss.
                Default is True.
    """
    asyncio.run(run_aerich_command("initialization", safe=safe))


@db_commands.command()
def make(
        app: Annotated[
            Optional[str],
            typer.Argument(help="The specific application to create migrations for. "
                                "If None, creates migrations for all registered applications.")]
        = None,
) -> None:
    """
    Create migrations for the specified application or all registered applications using Aerich.

    :param app: The specific application to create migrations for.
                If None, creates migrations for all registered applications.
    """
    asyncio.run(run_aerich_command("create migrations", app))


@db_commands.command()
def migrate(
        app: Annotated[
            Optional[str],
            typer.Argument(help="The specific application to apply migrations for. "
                                "If None, applies migrations for all registered applications.")]
        = None,
        transaction: bool = typer.Option(
            True, help="If True, run the operation within a transaction."
        ),
) -> None:
    """
    Apply migrations for the specified application or all registered applications using Aerich.

    :param app: The specific application to apply migrations for.
                If None, applies migrations for all registered applications.
    :param transaction: If True, run the operation within a transaction.
                               Default is True.
    """
    asyncio.run(run_aerich_command("apply migrations", app, transaction=transaction))


if __name__ == "__main__":
    db_commands()
# from aerich.migrate.Migrate