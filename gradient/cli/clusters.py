from gradient.cli.cli import cli
from gradient.cli.common import ClickGroup, api_key_option


@cli.group("clusters", help="Manage clusters", cls=ClickGroup)
def clusters():
    pass

@clusters.command("list", help="List your team clusters")
@api_key_option
def get_clusters_list(api_key):
    pass
