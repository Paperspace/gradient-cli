import getpass

import click

from gradient.api_sdk.config import client, config
from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.validators import validate_email
from gradient.commands import login as login_commands


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


@cli.command("apiKey", help="Save your api key")
@click.argument("api_key", required=False, )
def save_api_key(api_key):
    if not api_key:
        api_key = getpass.getpass("Enter your API Key: ")

    command = login_commands.SetApiKeyCommand()
    api_key = api_key.strip()
    command.execute(api_key)
