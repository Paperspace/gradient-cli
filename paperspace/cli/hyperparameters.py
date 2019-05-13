import click

from paperspace import client, config
from paperspace.cli import common
from paperspace.cli.cli import cli
from paperspace.cli.common import ClickGroup
from paperspace.commands import hyperparameters as hyperparameters_commands


@cli.group("hyperparameters", help="Manage hyperparameters", cls=ClickGroup)
def hyperparameters_group():
    pass


@hyperparameters_group.command("create", help="Create hyperparameter")
@click.option(
    "--name",
    "name",
    required=True,
)
@click.option(
    "--projectId",
    "projectHandle",
    required=True,
)
@click.option(
    "--tuningCommand",
    "tuningCommand",
    required=True,
)
@click.option(
    "--workerContainer",
    "workerContainer",
    required=True,
)
@click.option(
    "--workerMachineType",
    "workerMachineType",
    required=True,
)
@click.option(
    "--workerCommand",
    "workerCommand",
    required=True,
)
@click.option(
    "--workerCount",
    "workerCount",
    required=True,
    type=int,
)
@click.option(
    "--serverRegistryUsername",
    "hyperparameterServerRegistryUsername",
)
@click.option(
    "--serverRegistryPassword",
    "hyperparameterServerRegistryPassword",
)
@click.option(
    "--serverContainerUser",
    "hyperparameterServerContainerUser",
)
@common.api_key_option
def create_hyperparameter(api_key, **hyperparameter):
    common.del_if_value_is_none(hyperparameter)
    hyperparameters_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    command = hyperparameters_commands.CreateHyperparameterCommand(api=hyperparameters_api)
    command.execute(hyperparameter)


@hyperparameters_group.command("list", help="List hyperparameters")
@common.api_key_option
def create_hyperparameter(api_key):
    hyperparameters_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    command = hyperparameters_commands.ListHyperparametersCommand(api=hyperparameters_api)
    command.execute()
