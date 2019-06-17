import getpass

import click

from gradient import logger
from gradient.cli.cli import cli
from gradient.commands import login as login_commands

LOGIN_DEPRECATION_MESSAGE = """The login command is currently disabled for logging in using `--email` and `--password`.

Instead, obtain an API Key from https://www.paperspace.com/console/account/api.

Then use the `apiKey` command to save your API Key locally.

Visit the docs @ https://docs.paperspace.com for more info!"""


@cli.command("login", help=LOGIN_DEPRECATION_MESSAGE, hidden=True)
@click.option(
    "--email",
    "email",
    help="Email used to create Paperspace account",
)
@click.option(
    "--password",
    "password",
    help="Password used to create Paperspace account",
)
@click.option(
    "--apiTokenName",
    "api_token_name",
    help="Name of api token used to log in",
)
def login(**kwargs):
    logger.warning(LOGIN_DEPRECATION_MESSAGE)


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
