import typer

example_commands = typer.Typer(name="appexample", help="Example commands")


@example_commands.command()
def hello_world():
    print("Hello World!")
