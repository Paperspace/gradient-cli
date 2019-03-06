import click

from paperspace import commands


def del_if_value_is_none(d):
    """Remove all elements with value == None"""
    for key, val in list(d.items()):
        if val is None:
            del d[key]


@click.group()
def cli():
    pass


@cli.group()
def experiments():
    pass


@experiments.group()
def create():
    pass


@create.command()
@click.option("--name", required=True)
@click.option("--experimentTypeId", "experimentTypeId", type=int, required=True)
@click.option("--workerCount", "workerCount", type=int, required=True)
@click.option("--workerContainer", "workerContainer", required=True)
@click.option("--workerMachineType", "workerMachineType", required=True)
@click.option("--workerCommand", "workerCommand", required=True)
@click.option("--parameterServerContainer", "parameterServerContainer", required=True)
@click.option("--parameterServerMachineType", "parameterServerMachineType", required=True)
@click.option("--parameterServerCommand", "parameterServerCommand", required=True)
@click.option("--parameterServerCount", "parameterServerCount", type=int, required=True)
@click.option("--ports", type=int)
@click.option("--workspaceUrl", "workspaceUrl")
@click.option("--projectHandler", "projectHandler")
@click.option("--workingDirectory", "workingDirectory")
@click.option("--artifactDirectory", "artifactDirectory")
@click.option("--clusterId", "clusterId", type=int)
# @click.option("--experimentEnv", type=dict)
@click.option("--workerContainerUser", "workerContainerUser")
@click.option("--workerRegistryUsername", "workerRegistryUsername")
@click.option("--workerRegistryPassword", "workerRegistryPassword")
@click.option("--parameterServerContainerUser", "parameterServerContainerUser")
@click.option("--parameterServerRegistryContainerUser", "parameterServerRegistryContainerUser")
@click.option("--parameterServerRegistryPassword", "parameterServerRegistryPassword")
def multinode(**kwargs):
    del_if_value_is_none(kwargs)
    commands.create_experiments(kwargs)
