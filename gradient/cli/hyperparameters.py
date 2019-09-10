import functools

import click

from gradient import utils
from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.common import ClickGroup
from gradient.cli.experiments import common_experiments_create_options, get_workspace_handler
from gradient.commands import hyperparameters as hyperparameters_commands


@cli.group("hyperparameters", help="Manage hyperparameters", cls=ClickGroup)
def hyperparameters_group():
    pass


def common_hyperparameter_create_options(f):
    options = [
        click.option(
            "--tuningCommand",
            "tuning_command",
            required=True,
            help="Tuning command",
            cls=common.GradientOption,
        ),
        click.option(
            "--workerContainer",
            "worker_container",
            required=True,
            help="Worker container",
            cls=common.GradientOption,
        ),
        click.option(
            "--workerContainerUser",
            "worker_container_user",
            required=False,
            help="Worker container user",
            cls=common.GradientOption,
        ),
        click.option(
            "--workerMachineType",
            "worker_machine_type",
            required=True,
            help="Worker machine type",
            cls=common.GradientOption,
        ),
        click.option(
            "--hyperparameterServerMachineType",
            "hyperparameter_server_machine_type",
            required=False,
            help="Hyperparameter Server machine type",
            cls=common.GradientOption,
        ),
        click.option(
            "--workerCommand",
            "worker_command",
            required=True,
            help="Worker command",
            cls=common.GradientOption,
        ),
        click.option(
            "--workerCount",
            "worker_count",
            required=True,
            type=int,
            help="Worker count",
            cls=common.GradientOption,
        ),
        click.option(
            "--workerUseDockerfile",
            "use_dockerfile",
            type=bool,
            is_flag=True,
            default=False,
            help="Flag: use dockerfile",
            cls=common.GradientOption,
        ),
        click.option(
            "--workerDockerfilePath",
            "dockerfile_path",
            help="Path to ",
            cls=common.GradientOption,
        ),
        click.option(
            "--workerRegistryUsername",
            "worker_registry_username",
            help="Worker registry username",
            cls=common.GradientOption,
        ),
        click.option(
            "--workerRegistryPassword",
            "worker_registry_password",
            help="Worker registry password",
            cls=common.GradientOption,
        ),
        click.option(
            "--hyperparameterServerRegistryUsername",
            "hyperparameter_server_registry_username",
            help="Hyperparameter server registry username",
            cls=common.GradientOption,
        ),
        click.option(
            "--hyperparameterServerRegistryPassword",
            "hyperparameter_server_registry_password",
            help="Hyperparameter server registry password",
            cls=common.GradientOption,
        ),
        click.option(
            "--hyperparameterServerContainer",
            "hyperparameter_server_container",
            help="Hyperparameter server container",
            cls=common.GradientOption,
        ),
        click.option(
            "--hyperparameterServerContainerUser",
            "hyperparameter_server_container_user",
            help="Hyperparameter server container user",
            cls=common.GradientOption,
        ),
    ]
    return functools.reduce(lambda x, opt: opt(x), reversed(options), f)


@hyperparameters_group.command("create", help="Create hyperparameter")
@common_experiments_create_options
@common_hyperparameter_create_options
@common.api_key_option
@common.options_file
def create_hyperparameter(api_key, options_file, **hyperparameter):
    utils.validate_workspace_input(hyperparameter)
    common.del_if_value_is_none(hyperparameter, del_all_falsy=True)

    command = hyperparameters_commands.CreateHyperparameterCommand(
        api_key=api_key,
        workspace_handler=get_workspace_handler(api_key),
    )
    command.execute(hyperparameter)


@hyperparameters_group.command("run", help="Create and start hyperparameter tuning job")
@common_experiments_create_options
@common_hyperparameter_create_options
@common.api_key_option
@common.options_file
def create_and_start_hyperparameter(api_key, options_file, **hyperparameter):
    utils.validate_workspace_input(hyperparameter)
    common.del_if_value_is_none(hyperparameter, del_all_falsy=True)

    command = hyperparameters_commands.CreateAndStartHyperparameterCommand(
        api_key=api_key,
        workspace_handler=get_workspace_handler(api_key),
    )
    command.execute(hyperparameter)


@hyperparameters_group.command("list", help="List hyperparameters")
@common.api_key_option
@common.options_file
def list_hyperparameters(api_key, options_file):
    command = hyperparameters_commands.ListHyperparametersCommand(api_key=api_key)
    command.execute()


@hyperparameters_group.command("details", help="Show details of hyperparameter")
@click.option(
    "--id",
    "id_",
    required=True,
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def get_hyperparameter_details(api_key, id_, options_file):
    command = hyperparameters_commands.HyperparameterDetailsCommand(api_key=api_key)
    command.execute(id_)


@hyperparameters_group.command("start", help="Start hyperparameter tuning")
@click.option(
    "--id",
    "id_",
    required=True,
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def start_hyperparameter_tuning(api_key, options_file, id_):
    command = hyperparameters_commands.HyperparameterStartCommand(api_key=api_key)
    command.execute(id_)
