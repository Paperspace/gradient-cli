import click

from paperspace import client, config
from paperspace.cli.cli import cli
from paperspace.cli.validators import validate_email
from paperspace.commands import login as login_commands


@cli.command("login", help="Log in with email and password")
@click.option(
    "--email",
    "email",
    required=True,
    callback=validate_email,
    help="Email used to create Paperspace account",
)
@click.option(
    "--password",
    "password",
    prompt=True,
    hide_input=True,
    help="Password used to create Paperspace account",
)
@click.option(
    "--apiTokenName",
    "api_token_name",
    help="Name of api token used to log in",
)
def login(email, password, api_token_name):
    machines_api = client.API(config.CONFIG_HOST)
    command = login_commands.LogInCommand(api=machines_api)
    command.execute(email, password, api_token_name)


@cli.command("logout", help="Log out / remove apiKey from config file")
def logout():
    command = login_commands.LogOutCommand()
    command.execute()
