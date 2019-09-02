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
    "vp_type_id",
    required=True,
    help="Type of Virtual Machine",
    cls=common.OptionReadValueFromConfigFile,
)
@click.option(
    "--containerId",
    "container_id",
    # required=True,
    help="Container ID",
    cls=common.OptionReadValueFromConfigFile,
)
@click.option(
    "--containerName",
    "container_name",
    help="Container name",
    cls=common.OptionReadValueFromConfigFile,
)
@click.option(
    "--name",
    "name",
    help="Notebook name",
    cls=common.OptionReadValueFromConfigFile,
)
@click.option(
    "--clusterId",
    "cluster_id",
    help="Cluster ID",
    cls=common.OptionReadValueFromConfigFile,
)
@click.option(
    "--registryUsername",
    "registry_username",
    help="Registry username",
    cls=common.OptionReadValueFromConfigFile,
)
@click.option(
    "--registryPassword",
    "registry_password",
    help="Registry password",
    cls=common.OptionReadValueFromConfigFile,
)
@click.option(
    "--defaultEntrypoint",
    "default_entrypoint",
    help="Default entrypoint",
    cls=common.OptionReadValueFromConfigFile,
)
@click.option(
    "--containerUser",
    "container_user",
    help="Container user",
    cls=common.OptionReadValueFromConfigFile,
)
@click.option(
    "--shutdownTimeout",
    "shutdown_timeout",
    help="Shutdown timeout in hours",
    type=float,
    cls=common.OptionReadValueFromConfigFile,
)
@click.option(
    "--isPreemptible",
    "is_preemptible",
    help="Is preemptible",
    type=bool,
    cls=common.OptionReadValueFromConfigFile,
)
@common.api_key_option
@common.options_file
def create(api_key, options_file, **notebook):
    command = notebooks.CreateNotebookCommand(api_key=api_key)
    command.execute(**notebook)
