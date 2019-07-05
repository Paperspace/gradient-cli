import collections
import functools

import click

from gradient import client, config, constants, utils
from gradient.cli.cli import cli
from gradient.cli.cli_types import json_string, ChoiceType
from gradient.cli.common import api_key_option, del_if_value_is_none, ClickGroup, deprecated
from gradient.commands import experiments as experiments_commands

MULTI_NODE_EXPERIMENT_TYPES_MAP = collections.OrderedDict(
    (
        ("GRPC", constants.ExperimentType.GRPC_MULTI_NODE),
        ("MPI", constants.ExperimentType.MPI_MULTI_NODE),
    )
)


@cli.group("experiments", help="Manage experiments", cls=ClickGroup)
def experiments():
    pass


@experiments.group("create", help="Create new experiment", cls=ClickGroup)
def create_experiment():
    pass


@experiments.group(name="run", help="Create and start new experiment", cls=ClickGroup)
def create_and_start_experiment():
    pass


def common_experiments_create_options(f):
    options = [
        click.option(
            "--name",
            required=True,
            help="Name of new experiment",
        ),
        click.option(
            "--ports",
            help="Port to use in new experiment",
        ),
        click.option(
            "--workspace",
            "workspace",
            help="Path to workspace directory",
        ),
        click.option(
            "--workspaceArchive",
            "workspaceArchive",
            help="Path to workspace .zip archive",
        ),
        click.option(
            "--workspaceUrl",
            "workspaceUrl",
            help="Project git repository url",
        ),
        click.option(
            "--ignoreFiles",
            "ignore_files",
            help="Ignore certain files from uploading"
        ),
        click.option(
            "--workingDirectory",
            "workingDirectory",
            help="Working directory for the experiment",
        ),
        click.option(
            "--artifactDirectory",
            "artifactDirectory",
            help="Artifacts directory",
        ),
        click.option(
            "--clusterId",
            "clusterId",
            help="Cluster ID",
        ),
        click.option(
            "--experimentEnv",
            "experimentEnv",
            type=json_string,
            help="Environment variables in a JSON",
        ),
        click.option(
            "--projectId",
            "projectHandle",
            required=True,
            help="Project ID",
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
        api_key_option
    ]
    return functools.reduce(lambda x, opt: opt(x), reversed(options), f)


def common_experiment_create_multi_node_options(f):
    options = [
        click.option(
            "--experimentType",
            "experimentTypeId",
            type=ChoiceType(MULTI_NODE_EXPERIMENT_TYPES_MAP, case_sensitive=False),
            required=True,
            help="Experiment Type",
        ),
        click.option(
            "--workerContainer",
            "workerContainer",
            required=True,
            help="Worker container",
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
            type=int,
            required=True,
            help="Worker count",
        ),
        click.option(
            "--parameterServerContainer",
            "parameterServerContainer",
            required=True,
            help="Parameter server container",
        ),
        click.option(
            "--parameterServerMachineType",
            "parameterServerMachineType",
            required=True,
            help="Parameter server machine type",
        ),
        click.option(
            "--parameterServerCommand",
            "parameterServerCommand",
            required=True,
            help="Parameter server command",
        ),
        click.option(
            "--parameterServerCount",
            "parameterServerCount",
            type=int,
            required=True,
            help="Parameter server count",
        ),
        click.option(
            "--workerContainerUser",
            "workerContainerUser",
            help="Worker container user",
        ),
        click.option(
            "--workerRegistryUsername",
            "workerRegistryUsername",
            help="Worker container registry username",
        ),
        click.option(
            "--workerRegistryPassword",
            "workerRegistryPassword",
            help="Worker registry password",
        ),
        click.option(
            "--parameterServerContainerUser",
            "parameterServerContainerUser",
            help="Parameter server container user",
        ),
        click.option(
            "--parameterServerRegistryContainerUser",
            "parameterServerRegistryContainerUser",
            help="Parameter server registry container user",
        ),
        click.option(
            "--parameterServerRegistryPassword",
            "parameterServerRegistryPassword",
            help="Parameter server registry password",
        ),
    ]
    return functools.reduce(lambda x, opt: opt(x), reversed(options), f)


def common_experiments_create_single_node_options(f):
    options = [
        click.option(
            "--container",
            required=True,
            help="Container",
        ),
        click.option(
            "--machineType",
            "machineType",
            required=True,
            help="Machine type",
        ),
        click.option(
            "--command",
            required=True,
            help="Container entrypoint command",
        ),
        click.option(
            "--containerUser",
            "containerUser",
            help="Container user",
        ),
        click.option(
            "--registryUsername",
            "registryUsername",
            help="Registry username",
        ),
        click.option(
            "--registryPassword",
            "registryPassword",
            help="Registry password",
        ),
    ]
    return functools.reduce(lambda x, opt: opt(x), reversed(options), f)


@deprecated("DeprecatedWarning: \nWARNING: --workspaceUrl and --workspaceArchive "
            "options will not be included in version 0.6.0")
@create_experiment.command(name="multinode", help="Create multi node experiment")
@common_experiments_create_options
@common_experiment_create_multi_node_options
def create_multi_node(api_key, **kwargs):
    utils.validate_workspace_input(kwargs)
    del_if_value_is_none(kwargs)
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    command = experiments_commands.CreateExperimentCommand(api=experiments_api)
    command.execute(kwargs)


@deprecated("DeprecatedWarning: \nWARNING: --workspaceUrl and --workspaceArchive "
            "options will not be included in version 0.6.0")
@create_experiment.command(name="singlenode", help="Create single node experiment")
@common_experiments_create_options
@common_experiments_create_single_node_options
def create_single_node(api_key, **kwargs):
    utils.validate_workspace_input(kwargs)
    kwargs["experimentTypeId"] = constants.ExperimentType.SINGLE_NODE
    del_if_value_is_none(kwargs)
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    command = experiments_commands.CreateExperimentCommand(api=experiments_api)
    command.execute(kwargs)


@deprecated("DeprecatedWarning: \nWARNING: --workspaceUrl and --workspaceArchive "
            "options will not be included in version 0.6.0")
@create_and_start_experiment.command(name="multinode", help="Create and start new multi node experiment")
@common_experiments_create_options
@common_experiment_create_multi_node_options
@click.option(
    "--no-logs",
    "show_logs",
    is_flag=True,
    flag_value=False,
    default=True,
    help="Don't show logs. Only create, start and exit",
)
@click.pass_context
def create_and_start_multi_node(ctx, api_key, show_logs, **kwargs):
    utils.validate_workspace_input(kwargs)
    del_if_value_is_none(kwargs)
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    command = experiments_commands.CreateAndStartExperimentCommand(api=experiments_api)
    experiment = command.execute(kwargs)
    if experiment and show_logs:
        ctx.invoke(list_logs, experiment_id=experiment["handle"], line=0, limit=100, follow=True, api_key=api_key)


@deprecated("DeprecatedWarning: \nWARNING: --workspaceUrl and --workspaceArchive "
            "options will not be included in version 0.6.0")
@create_and_start_experiment.command(name="singlenode", help="Create and start new single node experiment")
@common_experiments_create_options
@common_experiments_create_single_node_options
@click.option(
    "--no-logs",
    "show_logs",
    is_flag=True,
    flag_value=False,
    default=True,
    help="Don't show logs. Only create, start and exit",
)
@click.pass_context
def create_and_start_single_node(ctx, api_key, show_logs, **kwargs):
    utils.validate_workspace_input(kwargs)
    kwargs["experimentTypeId"] = constants.ExperimentType.SINGLE_NODE
    del_if_value_is_none(kwargs)
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    command = experiments_commands.CreateAndStartExperimentCommand(api=experiments_api)
    experiment = command.execute(kwargs)
    if experiment and show_logs:
        ctx.invoke(list_logs, experiment_id=experiment["handle"], line=0, limit=100, follow=True, api_key=api_key)


@experiments.command("start", help="Start experiment")
@click.argument("experiment-id")
@api_key_option
@click.option(
    "--logs",
    "show_logs",
    is_flag=True,
    help="Show logs",
)
@click.pass_context
def start_experiment(ctx, experiment_id, show_logs, api_key):
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    experiments_commands.start_experiment(experiment_id, api=experiments_api)
    if show_logs:
        ctx.invoke(list_logs, experiment_id=experiment_id, line=0, limit=100, follow=True, api_key=api_key)


@experiments.command("stop", help="Stop experiment")
@click.argument("experiment-id")
@api_key_option
def stop_experiment(experiment_id, api_key):
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    experiments_commands.stop_experiment(experiment_id, api=experiments_api)


@experiments.command("list", help="List experiments")
@click.option("--projectId", "-p", "project_ids", multiple=True)
@api_key_option
def list_experiments(project_ids, api_key):
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    command = experiments_commands.ListExperimentsCommand(api=experiments_api)
    command.execute(project_ids=project_ids)


@experiments.command("details", help="Show detail of an experiment")
@click.argument("experiment-id")
@api_key_option
def get_experiment_details(experiment_id, api_key):
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    experiments_commands.get_experiment_details(experiment_id, api=experiments_api)


@experiments.command("logs", help="List experiment logs")
@click.option(
    "--experimentId",
    "experiment_id",
    required=True
)
@click.option(
    "--line",
    "line",
    required=False,
    default=0
)
@click.option(
    "--limit",
    "limit",
    required=False,
    default=10000
)
@click.option(
    "--follow",
    "follow",
    required=False,
    default=False
)
@api_key_option
def list_logs(experiment_id, line, limit, follow, api_key=None):
    logs_api = client.API(config.CONFIG_LOG_HOST, api_key=api_key)
    command = experiments_commands.ExperimentLogsCommand(api=logs_api)
    command.execute(experiment_id, line, limit, follow)
