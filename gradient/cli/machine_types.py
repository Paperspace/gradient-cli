import click

from gradient.cli import common
from gradient.cli.clusters import clusters
from gradient.cli.common import api_key_option
from gradient.commands.machine_types import ListMachineTypesCommand


@clusters.group("machineTypes", help="Manage machine types")
def machine_types_group():
    pass


@machine_types_group.command("list", help="List available machine types")
@click.option(
    "--clusterId",
    "cluster_id",
    help="Filter machine types by cluster ID",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def list_machine_types(cluster_id=None, options_file=None, api_key=None):
    command = ListMachineTypesCommand(api_key=api_key)
    command.execute(cluster_id=cluster_id)
