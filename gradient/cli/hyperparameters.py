import functools

import click

from gradient import client, config
from gradient.cli import common, cli_types
from gradient.cli.cli import cli
from gradient.cli.common import ClickGroup
from gradient.commands import hyperparameters as hyperparameters_commands


def add_use_docker_file_flag_if_used(ctx, param, value):
    if value:
        ctx.params["useDockerFile"] = True

    return value


@cli.group("hyperparameters", help="Manage hyperparameters", cls=ClickGroup)
def hyperparameters_group():
    pass


def common_hyperparameter_create_options(f):
    options = [
        click.option(
            "--name",
            "name",
            required=True,
            help="Job name",
        ),
        click.option(
            "--projectId",
            "projectHandle",
            required=True,
            help="Project ID",
        ),
        click.option(
            "--tuningCommand",
            "tuningCommand",
            required=True,
            help="Tuning command",
        ),
        click.option(
            "--workerContainer",
            "workerContainer",
            required=True,
            help="Worker Docker image",
        ),
        click.option(
            "--workerMachineType",
            "workerMachineType",
            required=True,
            help="Worker machine type",
        ),
        click.option(
            "--workerCommand",
            "workerCommand",
            required=True,
            help="Worker command",
        ),
        click.option(
            "--workerCount",
            "workerCount",
            required=True,
            type=int,
            help="Worker count",
        ),
        click.option(
            "--isPreemptible",
            "isPreemptible",
            type=bool,
            is_flag=True,
            help="Flag: isPreemptible",
        ),
        click.option(
            "--ports",
            "ports",
            help="Port to use in new job",
        ),
        click.option(
            "--workspaceUrl",
            "workspaceUrl",
            help="Project git repository url",
        ),
        click.option(
            "--artifactDirectory",
            "artifactDirectory",
            help="Artifacts directory",
        ),
        click.option(
            "--clusterId",
            "clusterId",
            type=int,
            help="Cluster ID",
        ),
        click.option(
            "--experimentEnv",
            "experimentEnv",
            type=cli_types.json_string,
            help="Environment variables in a JSON",
        ),
        click.option(
            "--triggerEventId",
            "triggerEventId",
            type=int,
            help="Trigger event ID",
        ),
        click.option(
            "--modelType",
            "modelType",
            help="Model type",
        ),
        click.option(
            "--modelPath",
            "modelPath",
            help="Model path",
        ),
        click.option(
            "--dockerfilePath",
            "dockerfilePath",
            callback=add_use_docker_file_flag_if_used,
            help="Path to Dockerfile",
        ),
        click.option(
            "--serverRegistryUsername",
            "hyperparameterServerRegistryUsername",
            help="Hyperparameter server registry username",
        ),
        click.option(
            "--serverRegistryPassword",
            "hyperparameterServerRegistryPassword",
            help="Hyperparameter server registry password",
        ),
        click.option(
            "--serverContainerUser",
            "hyperparameterServerContainerUser",
            help="Hyperparameter server container user",
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


@hyperparameters_group.command("run", help="Create and start hyperparameter tuning job")
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
