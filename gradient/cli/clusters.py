import click

from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.common import ClickGroup, api_key_option
from gradient.commands.clusters import ListClustersCommand


@cli.group("clusters", help="Manage clusters", cls=ClickGroup)
def clusters():
    pass


@clusters.command("list", help="List your team clusters")
@click.option(
    "--limit",
    "-l",
    "cluster_limit",
    default=20,
    help="Limit listed experiments per page",
    cls=common.GradientOption,
)
@click.option(
    "--offset",
    "-o",
    "cluster_offset",
    default=0,
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def get_clusters_list(api_key, cluster_limit, cluster_offset, options_file):
    command = ListClustersCommand(api_key=api_key)

    res = command.execute(limit=cluster_limit, offset=cluster_offset)

    for cluster_str, next_iteration in res:
        click.echo(cluster_str)
        if next_iteration:
            click.confirm("Do you want to continue?", abort=True)
