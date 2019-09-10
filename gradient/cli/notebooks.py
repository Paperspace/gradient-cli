import click

from gradient.cli import common
from gradient.cli.cli import cli
from gradient.commands import notebooks


@cli.group("notebooks", help="Manage notebooks", cls=common.ClickGroup)
def notebooks_group():
    pass


@notebooks_group.command("create", help="Create new notebook")
@click.option(
    "--vmTypeId",
    "vm_type_id",
    type=int,
    required=True,
    help="Type of Virtual Machine",
    cls=common.GradientOption,
)
@click.option(
    "--containerId",
    "container_id",
    type=int,
    required=True,
    help="Container ID",
    cls=common.GradientOption,
)
@click.option(
    "--clusterId",
    "cluster_id",
    type=int,
    required=True,
    help="Cluster ID",
    cls=common.GradientOption,
)
@click.option(
    "--containerName",
    "container_name",
    help="Container name",
    cls=common.GradientOption,
)
@click.option(
    "--name",
    "name",
    help="Notebook name",
    cls=common.GradientOption,
)
@click.option(
    "--registryUsername",
    "registry_username",
    help="Registry username",
    cls=common.GradientOption,
)
@click.option(
    "--registryPassword",
    "registry_password",
    help="Registry password",
    cls=common.GradientOption,
)
@click.option(
    "--defaultEntrypoint",
    "default_entrypoint",
    help="Default entrypoint",
    cls=common.GradientOption,
)
@click.option(
    "--containerUser",
    "container_user",
    help="Container user",
    cls=common.GradientOption,
)
@click.option(
    "--shutdownTimeout",
    "shutdown_timeout",
    help="Shutdown timeout in hours",
    type=float,
    cls=common.GradientOption,
)
@click.option(
    "--isPreemptible",
    "is_preemptible",
    help="Is preemptible",
    is_flag=True,
    type=bool,
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def create_notebook(api_key, options_file, **notebook):
    command = notebooks.CreateNotebookCommand(api_key=api_key)
    command.execute(**notebook)


@notebooks_group.command("delete", help="Delete existing notebook")
@click.option(
    "--id",
    "id_",
    help="Notebook ID",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def delete_notebook(id_, api_key, options_file):
    command = notebooks.DeleteNotebookCommand(api_key=api_key)
    command.execute(id_=id_)


@notebooks_group.command("list", help="List notebooks")
@common.api_key_option
@common.options_file
def list_notebooks(api_key, options_file):
    command = notebooks.ListNotebooksCommand(api_key=api_key)
    command.execute()


@notebooks_group.command("show", help="Show notebook details", hidden=True)
@click.option(
    "--id",
    "id",
    help="Notebook ID",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def show_notebook(id, api_key, options_file):
    command = notebooks.ShowNotebookDetailsCommand(api_key=api_key)
    command.execute(id)
