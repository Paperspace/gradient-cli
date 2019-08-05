import collections
import functools

import click

from gradient import constants, utils, logger, workspace
from gradient.api_sdk.clients import http_client
from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.cli_types import json_string, ChoiceType
from gradient.cli.common import api_key_option, ClickGroup, deprecated
from gradient.commands import experiments as experiments_commands
from gradient.config import config

MULTI_NODE_EXPERIMENT_TYPES_MAP = collections.OrderedDict(
    (
        ("GRPC", constants.ExperimentType.GRPC_MULTI_NODE),
        ("MPI", constants.ExperimentType.MPI_MULTI_NODE),
    )
)


def get_workspace_handler(api_key):
    client = http_client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    logger_ = logger.Logger()
    workspace_handler = workspace.S3WorkspaceHandlerWithProgressbar(experiments_api=client, logger_=logger_)
    return workspace_handler


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
            help="Path to workspace directory, archive, S3 or git repository",
        ),
        click.option(
            "--workspaceArchive",
            "workspace_archive",
            help="Path to workspace .zip archive",
        ),
        click.option(
            "--workspaceUrl",
            "workspace_url",
            help="Project git repository url",
        ),
        click.option(
            "--ignoreFiles",
            "ignore_files",
            help="Ignore certain files from uploading"
        ),
        click.option(
            "--workingDirectory",
            "working_directory",
            help="Working directory for the experiment",
        ),
        click.option(
            "--artifactDirectory",
            "artifact_directory",
            help="Artifacts directory",
        ),
        click.option(
            "--clusterId",
            "cluster_id",
            help="Cluster ID",
        ),
        click.option(
            "--experimentEnv",
            "experiment_env",
            type=json_string,
            help="Environment variables in a JSON",
        ),
        click.option(
            "--projectId",
            "project_id",
            required=True,
            help="Project ID",
        ),
        click.option(
            "--modelType",
            "model_type",
            help="Model type",
        ),
        click.option(
            "--modelPath",
            "model_path",
            help="Model path",
        ),
        click.option(
            "--isPreemptible",
            "is_preemptible",
            type=bool,
            is_flag=True,
            help="Flag: is preemptible",
        ),
        api_key_option
    ]
    return functools.reduce(lambda x, opt: opt(x), reversed(options), f)


def common_experiment_create_multi_node_options(f):
    options = [
        click.option(
            "--experimentType",
            "experiment_type_id",
            type=ChoiceType(MULTI_NODE_EXPERIMENT_TYPES_MAP, case_sensitive=False),
            required=True,
            help="Experiment Type",
        ),
        click.option(
            "--workerContainer",
            "worker_container",
            required=True,
            help="Worker container",
        ),
        click.option(
            "--workerMachineType",
            "worker_machine_type",
            required=True,
            help="Worker machine type",
        ),
        click.option(
            "--workerCommand",
            "worker_command",
            required=True,
            help="Worker command",
        ),
        click.option(
            "--workerCount",
            "worker_count",
            type=int,
            required=True,
            help="Worker count",
        ),
        click.option(
            "--parameterServerContainer",
            "parameter_server_container",
            required=True,
            help="Parameter server container",
        ),
        click.option(
            "--parameterServerMachineType",
            "parameter_server_machine_type",
            required=True,
            help="Parameter server machine type",
        ),
        click.option(
            "--parameterServerCommand",
            "parameter_server_command",
            required=True,
            help="Parameter server command",
        ),
        click.option(
            "--parameterServerCount",
            "parameter_server_count",
            type=int,
            required=True,
            help="Parameter server count",
        ),
        click.option(
            "--workerContainerUser",
            "worker_container_user",
            help="Worker container user",
        ),
        click.option(
            "--workerRegistryUsername",
            "worker_registry_username",
            help="Worker container registry username",
        ),
        click.option(
            "--workerRegistryPassword",
            "worker_registry_password",
            help="Worker registry password",
        ),
        click.option(
            "--workerRegistryUrl",
            "worker_registry_url",
            help="Worker registry URL",
        ),
        click.option(
            "--parameterServerContainerUser",
            "parameter_server_container_user",
            help="Parameter server container user",
        ),
        click.option(
            "--parameterServerRegistryUsername",
            "parameter_server_registry_username",
            help="Parameter server registry username",
        ),
        click.option(
            "--parameterServerRegistryPassword",
            "parameter_server_registry_password",
            help="Parameter server registry password",
        ),
        click.option(
            "--parameterServerRegistryUrl",
            "parameter_server_registry_url",
            help="Parameter server registry URL",
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
            "machine_type",
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
            "container_user",
            help="Container user",
        ),
        click.option(
            "--registryUsername",
            "registry_username",
            help="Registry username",
        ),
        click.option(
            "--registryPassword",
            "registry_password",
            help="Registry password",
        ),
        click.option(
            "--registryUrl",
            "registry_url",
            help="Registry URL",
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
    common.del_if_value_is_none(kwargs, del_all_falsy=True)

    command = experiments_commands.CreateMultiNodeExperimentCommand(
        api_key=api_key,
        workspace_handler=get_workspace_handler(api_key),
    )
    command.execute(kwargs)


@deprecated("DeprecatedWarning: \nWARNING: --workspaceUrl and --workspaceArchive "
            "options will not be included in version 0.6.0")
@create_experiment.command(name="singlenode", help="Create single node experiment")
@common_experiments_create_options
@common_experiments_create_single_node_options
def create_single_node(api_key, **kwargs):
    utils.validate_workspace_input(kwargs)
    common.del_if_value_is_none(kwargs, del_all_falsy=True)

    command = experiments_commands.CreateSingleNodeExperimentCommand(
        api_key=api_key,
        workspace_handler=get_workspace_handler(api_key),
    )
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
    common.del_if_value_is_none(kwargs, del_all_falsy=True)

    command = experiments_commands.CreateAndStartMultiNodeExperimentCommand(
        api_key=api_key,
        workspace_handler=get_workspace_handler(api_key),
    )
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
    common.del_if_value_is_none(kwargs, del_all_falsy=True)

    command = experiments_commands.CreateAndStartSingleNodeExperimentCommand(
        api_key=api_key,
        workspace_handler=get_workspace_handler(api_key),
    )
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
    command = experiments_commands.StartExperimentCommand(api_key=api_key)
    command.execute(experiment_id)

    if show_logs:
        ctx.invoke(list_logs, experiment_id=experiment_id, line=0, limit=100, follow=True, api_key=api_key)


@experiments.command("stop", help="Stop experiment")
@click.argument("experiment-id")
@api_key_option
def stop_experiment(experiment_id, api_key):
    command = experiments_commands.StopExperimentCommand(api_key=api_key)
    command.execute(experiment_id)


@experiments.command("list", help="List experiments")
@click.option("--projectId", "-p", "project_ids", multiple=True)
@api_key_option
def list_experiments(project_ids, api_key):
    command = experiments_commands.ListExperimentsCommand(api_key=api_key)
    command.execute(project_id=project_ids)


@experiments.command("details", help="Show detail of an experiment")
@click.argument("experiment-id")
@api_key_option
def get_experiment_details(experiment_id, api_key):
    command = experiments_commands.GetExperimentCommand(api_key=api_key)
    command.execute(experiment_id)


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
    command = experiments_commands.ExperimentLogsCommand(api_key=api_key)
    command.execute(experiment_id, line, limit, follow)
