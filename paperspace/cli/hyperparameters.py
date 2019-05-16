import functools

import click

from paperspace import client, config
from paperspace.cli import common
from paperspace.cli.cli import cli
from paperspace.cli.common import ClickGroup
from paperspace.commands import hyperparameters as hyperparameters_commands


@cli.group("hyperparameters", help="Manage hyperparameters", cls=ClickGroup)
def hyperparameters_group():
    pass


def common_hyperparameter_create_options(f):
    options = [
        click.option(
            "--name",
            "name",
            required=True,
        ),
        click.option(
            "--projectId",
            "projectHandle",
            required=True,
        ),
        click.option(
            "--tuningCommand",
            "tuningCommand",
            required=True,
        ),
        click.option(
            "--workerContainer",
            "workerContainer",
            required=True,
        ),
        click.option(
            "--workerMachineType",
            "workerMachineType",
            required=True,
        ),
        click.option(
            "--workerCommand",
            "workerCommand",
            required=True,
        ),
        click.option(
            "--workerCount",
            "workerCount",
            required=True,
            type=int,
        ),
        click.option(
            "--serverRegistryUsername",
            "hyperparameterServerRegistryUsername",
        ),
        click.option(
            "--serverRegistryPassword",
            "hyperparameterServerRegistryPassword",
        ),
        click.option(
            "--serverContainerUser",
            "hyperparameterServerContainerUser",
        ),
    ]
    return functools.reduce(lambda x, opt: opt(x), reversed(options), f)


@hyperparameters_group.command("create", help="Create hyperparameter")
@common_hyperparameter_create_options
@common.api_key_option
def create_hyperparameter(api_key, **hyperparameter):
    common.del_if_value_is_none(hyperparameter)
    hyperparameters_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    command = hyperparameters_commands.CreateHyperparameterCommand(api=hyperparameters_api)
    command.execute(hyperparameter)


@hyperparameters_group.command("createAndStart", help="Create hyperparameter")
@common_hyperparameter_create_options
@common.api_key_option
def create_and_start_hyperparameter(api_key, **hyperparameter):
    common.del_if_value_is_none(hyperparameter)
    hyperparameters_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    command = hyperparameters_commands.CreateAndStartHyperparameterCommand(api=hyperparameters_api)
    command.execute(hyperparameter)


@hyperparameters_group.command("list", help="List hyperparameters")
@common.api_key_option
def list_hyperparameters(api_key):
    hyperparameters_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    command = hyperparameters_commands.ListHyperparametersCommand(api=hyperparameters_api)
    command.execute()


# TODO: 'unhidden' command and test it when api is updated to support deleting hyperparameters
@hyperparameters_group.command("delete", help="Delete hyperparameter", hidden=True)
@click.option(
    "--id",
    "id_",
    required=True,
)
@common.api_key_option
def delete_hyperparameter(api_key, id_):
    hyperparameters_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    command = hyperparameters_commands.DeleteHyperparameterCommand(api=hyperparameters_api)
    command.execute(id_)


@hyperparameters_group.command("details", help="Show details of hyperparameter")
@click.option(
    "--id",
    "id_",
    required=True,
)
@common.api_key_option
def get_hyperparameter_details(api_key, id_):
    hyperparameters_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    command = hyperparameters_commands.HyperparameterDetailsCommand(api=hyperparameters_api)
    command.execute(id_)


@hyperparameters_group.command("start", help="Start hyperparameter tuning")
@click.option(
    "--id",
    "id_",
    required=True,
)
@common.api_key_option
def start_hyperparameter_tuning(api_key, id_):
    hyperparameters_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    command = hyperparameters_commands.HyperparameterStartCommand(api=hyperparameters_api)
    command.execute(id_)
