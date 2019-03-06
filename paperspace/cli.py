import click

from paperspace import commands


class OptionRequiredIfMultinode(click.Option):
    def full_process_value(self, ctx, value):
        value = super(OptionRequiredIfMultinode, self).full_process_value(ctx, value)

        if value is None and ctx.params["workercount"] > 1:
            msg = "Required if --workerCount > 1"
            raise click.MissingParameter(ctx=ctx, param=self, message=msg)

        return value


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


@experiments.command()
@click.option("--name", required=True)
@click.option("--workerCount", "workerCount", required=True, type=int)
@click.option("--workerContainer", "workerContainer", cls=OptionRequiredIfMultinode)
@click.option("--workerMachineType", "workerMachineType", cls=OptionRequiredIfMultinode)
@click.option("--workerCommand", "workerCommand", cls=OptionRequiredIfMultinode)
@click.option("--parameterServerContainer", "parameterServerContainer", cls=OptionRequiredIfMultinode)
@click.option("--parameterServerMachineType", "parameterServerMachineType", cls=OptionRequiredIfMultinode)
@click.option("--parameterServerCommand", "parameterServerCommand", cls=OptionRequiredIfMultinode)
@click.option("--parameterServerCount", "parameterServerCount", type=int, cls=OptionRequiredIfMultinode)
@click.option("--ports", type=int)
@click.option("--workspaceUrl", "workspaceUrl")
@click.option("--projectHandler", "projectHandler")
@click.option("--workingDirectory", "workingDirectory")
@click.option("--artifactDirectory", "artifactDirectory")
@click.option("--clusterId", "clusterId", type=int)
# @click.option("--experimentEnv", type=dict)
@click.option("--experimentTypeId", "experimentTypeId", type=int)
@click.option("--workerContainerUser", "workerContainerUser")
@click.option("--workerRegistryUsername", "workerRegistryUsername")
@click.option("--workerRegistryPassword", "workerRegistryPassword")
@click.option("--parameterServerContainerUser", "parameterServerContainerUser")
@click.option("--parameterServerRegistryContainerUser", "parameterServerRegistryContainerUser")
@click.option("--parameterServerRegistryPassword", "parameterServerRegistryPassword")
def create(**kwargs):
    del_if_value_is_none(kwargs)
    commands.create_experiments(kwargs)
