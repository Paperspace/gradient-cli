import click
from click_didyoumean import DYMGroup

from paperspace import client, config
from paperspace.commands import projects as projects_commands
from . import common


@click.group("projects", help="Manage projects", cls=DYMGroup)
def projects_group():
    pass


@projects_group.command("list", help="List projects")
@common.api_key_option
def delete_job(api_key):
    projects_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = projects_commands.ListProjectsCommand(api=projects_api)
    command.execute()
