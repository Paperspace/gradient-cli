from paperspace import client, config
from paperspace.cli.cli import cli
from paperspace.commands import projects as projects_commands
from paperspace.cli import common


@cli.group("projects", help="Manage projects", cls=common.ClickGroup)
def projects_group():
    pass


@projects_group.command("list", help="List projects")
@common.api_key_option
def delete_job(api_key):
    projects_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = projects_commands.ListProjectsCommand(api=projects_api)
    command.execute()
