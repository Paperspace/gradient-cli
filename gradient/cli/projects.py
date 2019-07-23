import click

from gradient.cli import common
from gradient.cli.cli import cli
from gradient.commands import projects as projects_commands
from gradient.wizards.projects import run_create_project_wizard


@cli.group("projects", help="Manage projects", cls=common.ClickGroup)
def projects_group():
    pass


@projects_group.command("list", help="List projects")
@common.api_key_option
def list_projects(api_key):
    command = projects_commands.ListProjectsCommand(api_key=api_key)
    command.execute()


@projects_group.command("create", help="Create project")
@click.option(
    "--name",
    "name",
    required=True,
    help="Name of new project",
)
@click.option(
    "--repositoryName",
    "repository_name",
    help="Name of the repository",
)
@click.option(
    "--repositoryUrl",
    "repository_url",
    help="URL to the repository",
)
@common.api_key_option
def create_project(api_key, **project):
    command = projects_commands.CreateProjectCommand(api_key)
    command.execute(project)


@projects_group.command("wizard", help="Run create project wizard")
def create_project_wizard():
    run_create_project_wizard()
