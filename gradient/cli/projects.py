import click

from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.common import validate_comma_split_option
from gradient.commands import projects as projects_commands


@cli.group("projects", help="Manage projects", cls=common.ClickGroup)
def projects_group():
    pass


@projects_group.group("tags", help="Manage project tags", cls=common.ClickGroup)
def project_tags():
    pass


@projects_group.command("list", help="List projects")
@click.option(
    "--tag",
    "tags",
    multiple=True,
    cls=common.GradientOption,
    help="Filter by tags. Multiple use"
)
@common.api_key_option
@common.options_file
def list_projects(api_key, tags, options_file):
    command = projects_commands.ListProjectsCommand(api_key=api_key)
    command.execute(tags=tags)


@projects_group.command("create", help="Create project")
@click.option(
    "--name",
    "name",
    required=True,
    help="Name of new project",
    cls=common.GradientOption,
)
@click.option(
    "--repositoryName",
    "repository_name",
    help="Name of the repository",
    cls=common.GradientOption,
)
@click.option(
    "--repositoryUrl",
    "repository_url",
    help="URL to the repository",
    cls=common.GradientOption,
)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    help="One or many tags that you want to add to experiment",
    cls=common.GradientOption
)
@click.option(
    "--tags",
    "tags_comma",
    help="Separated by comma tags that you want add to experiment",
    cls=common.GradientOption
)
@common.api_key_option
@common.options_file
def create_project(api_key, options_file, **project):
    project["tags"] = validate_comma_split_option(project.pop("tags_comma"), project.pop("tags"))
    command = projects_commands.CreateProjectCommand(api_key)
    command.execute(project)


@projects_group.command("details", help="Show details of a project")
@click.option(
    "--id",
    "project_id",
    required=True,
    help="Project ID",
)
@common.api_key_option
@common.options_file
def create_project(project_id, api_key, options_file):
    command = projects_commands.ShowProjectDetailsCommand(api_key)
    command.execute(project_id)


@projects_group.command("delete", help="Delete project and all its experiments")
@click.option(
    "--id",
    "project_id",
    required=True,
    help="ID of project",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def delete_project(project_id, options_file, api_key):
    command = projects_commands.DeleteProjectCommand(api_key)
    command.execute(project_id)


@project_tags.command("add", help="Add tags to project")
@click.option(
    "--id",
    "id",
    required=True,
    cls=common.GradientOption,
    help="ID of the project",
)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    help="One or many tags that you want to add to project",
    cls=common.GradientOption
)
@click.option(
    "--tags",
    "tags_comma",
    help="Separated by comma tags that you want add to project",
    cls=common.GradientOption
)
@common.api_key_option
@common.options_file
def project_add_tag(id, options_file, api_key, **kwargs):
    kwargs["tags"] = validate_comma_split_option(kwargs.pop("tags_comma"), kwargs.pop("tags"), raise_if_no_values=True)

    command = projects_commands.ProjectAddTagsCommand(api_key=api_key)
    command.execute(id, **kwargs)


@project_tags.command("remove", help="Remove tags from project")
@click.option(
    "--id",
    "id",
    required=True,
    cls=common.GradientOption,
    help="ID of the project",
)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    help="One or many tags that you want to remove from project",
    cls=common.GradientOption
)
@click.option(
    "--tags",
    "tags_comma",
    help="Separated by comma tags that you want to remove from project",
    cls=common.GradientOption
)
@common.api_key_option
@common.options_file
def project_remove_tags(id, options_file, api_key, **kwargs):
    kwargs["tags"] = validate_comma_split_option(kwargs.pop("tags_comma"), kwargs.pop("tags"), raise_if_no_values=True)

    command = projects_commands.ProjectRemoveTagsCommand(api_key=api_key)
    command.execute(id, **kwargs)
