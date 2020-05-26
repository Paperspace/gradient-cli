import functools

import click

from gradient import clilogger
from gradient.api_sdk import constants, workspace
from gradient.cli import common, validators
from gradient.cli.cli import cli
from gradient.cli.cli_types import json_string, ChoiceType
from gradient.cli.common import api_key_option, ClickGroup, validate_comma_split_option
from gradient.cli.utils.flag_with_value import GradientRegisterReaderOption, GradientRegisterWriterOption, \
    GradientRegisterWriterCommand
from gradient.cli_constants import CLI_PS_CLIENT_NAME
from gradient.commands import experiments as experiments_commands
from gradient.commands.experiments import ExperimentAddTagsCommand, ExperimentRemoveTagsCommand, \
    GetExperimentMetricsCommand, StreamExperimentMetricsCommand

MULTI_NODE_CREATE_EXPERIMENT_COMMANDS = {
    constants.ExperimentType.GRPC_MULTI_NODE: experiments_commands.CreateMultiNodeExperimentCommand,
    constants.ExperimentType.MPI_MULTI_NODE: experiments_commands.CreateMpiMultiNodeExperimentCommand,
}

MULTI_NODE_RUN_EXPERIMENT_COMMANDS = {
    constants.ExperimentType.GRPC_MULTI_NODE: experiments_commands.CreateAndStartMultiNodeExperimentCommand,
    constants.ExperimentType.MPI_MULTI_NODE: experiments_commands.CreateAndStartMpiMultiNodeExperimentCommand,
}


def get_workspace_handler(api_key):
    logger_ = clilogger.CliLogger()
    workspace_handler = workspace.S3WorkspaceHandlerWithProgressbar(api_key=api_key, logger_=logger_,
                                                                    client_name=CLI_PS_CLIENT_NAME)
    return workspace_handler


@cli.group("experiments", help="Manage experiments", cls=ClickGroup)
def experiments_group():
    pass


@experiments_group.group("create", help="Create new experiment", cls=ClickGroup)
def create_experiment():
    pass


@experiments_group.group(name="run", help="Create and start new experiment", cls=ClickGroup)
def create_and_start_experiment():
    pass


@experiments_group.group(name="tags", help="Manage tags for experiment", cls=ClickGroup)
def experiments_tags():
    pass


@experiments_group.group(name="metrics", help="Read experiment metrics", cls=ClickGroup)
def experiments_metrics():
    pass


def common_experiments_create_options(f):
    options = [
        click.option(
            "--name",
            metavar="<name>",
            help="Name of new experiment",
            cls=common.GradientOption,
        ),
        click.option(
            "--ports",
            help="Port to use in new experiment",
            cls=common.GradientOption,
            ),
            click.option(
                "--workspace",
                "workspace",
                help="Path to workspace directory, archive, S3 or git repository",
                default="none",
                cls=common.GradientOption,
            ),
            click.option(
                "--workspaceRef",
                "workspace_ref",
                help="Git commit hash, branch name or tag",
                cls=common.GradientOption,
            ),
            click.option(
                "--workspaceUsername",
                "workspace_username",
                metavar="<username>",
                help="Workspace username",
                cls=common.GradientOption,
            ),
            click.option(
                "--workspacePassword",
                "workspace_password",
                help="Workspace password",
                cls=common.GradientOption,
            ),
        click.option(
            "--ignoreFiles",
            "ignore_files",
            help="Ignore certain files from uploading",
            cls=common.GradientOption,
        ),
        click.option(
            "--workingDirectory",
            "working_directory",
            help="Working directory for the experiment",
            cls=common.GradientOption,
        ),
        click.option(
            "--artifactDirectory",
            "artifact_directory",
            help="Artifacts directory",
            cls=common.GradientOption,
        ),
        click.option(
            "--clusterId",
            "cluster_id",
            metavar="<cluster ID>",
            help="Cluster ID",
            cls=common.GradientOption,
        ),
        click.option(
            "--experimentEnv",
            "experiment_env",
            type=json_string,
            help="Environment variables in a JSON",
            cls=common.GradientOption,
        ),
        click.option(
            "--projectId",
            "project_id",
            metavar="<project ID>",
            required=True,
            help="Project ID",
            cls=common.GradientOption,
        ),
        click.option(
            "--modelType",
            "model_type",
            metavar="<model type>",
            help="Model type",
            cls=common.GradientOption,
        ),
        click.option(
            "--modelPath",
            "model_path",
            metavar="<path>",
            help="Model path",
            cls=common.GradientOption,
        ),
        click.option(
            "--isPreemptible",
            "is_preemptible",
            type=bool,
            is_flag=True,
            help="Flag: is preemptible",
            cls=common.GradientOption,
        ),
        click.option(
            "--tag",
            "tags",
            multiple=True,
            help="One or many tags that you want to add to experiment",
            cls=common.GradientOption
        ),
        click.option(
            "--tags",
            "tags_comma",
            help="Separated by comma tags that you want add to experiment",
            cls=common.GradientOption
        )
    ]
    return functools.reduce(lambda x, opt: opt(x), reversed(options), f)


def dataset_options(f):
    options = [
        click.option(
            "--datasetUri",
            "dataset_uri_list",
            metavar="<dateset uri>",
            multiple=True,
            help="Url to S3 bucket with dataset",
            cls=common.GradientDatasetOption,
        ),
        click.option(
            "--datasetName",
            "dataset_name_list",
            multiple=True,
            metavar="<dateset name>",
            help="Name of dataset",
            cls=common.GradientDatasetOption,
        ),
        click.option(
            "--datasetAwsAccessKeyId",
            "dataset_access_key_id_list",
            multiple=True,
            metavar="<AWS access key>",
            help="S3 bucket's Access Key ID",
            cls=common.GradientDatasetOption,
        ),
        click.option(
            "--datasetAwsSecretAccessKey",
            "dataset_secret_access_key_list",
            multiple=True,
            help="S3 bucket's Secret Access Key",
            cls=common.GradientDatasetOption,
        ),
        click.option(
            "--datasetVersionId",
            "dataset_version_id_list",
            metavar="<version ID>",
            multiple=True,
            help="S3 dataset's version ID",
            cls=common.GradientDatasetOption,
        ),
        click.option(
            "--datasetEtag",
            "dataset_etag_list",
            metavar="<etag>",
            multiple=True,
            help="S3 dataset's ETag",
            cls=common.GradientDatasetOption,
        ),
        click.option(
            "--datasetVolumeKind",
            "dataset_volume_kind_list",
            multiple=True,
            type=ChoiceType(constants.DATASET_VOLUME_KINDS, case_sensitive=False),
            help="S3 dataset's volume kind. If used, --datasetVolumeSize has to be set as well",
            cls=common.GradientDatasetOption,
        ),
        click.option(
            "--datasetVolumeSize",
            "dataset_volume_size_list",
            multiple=True,
            help="S3 dataset's volume size",
            cls=common.GradientDatasetOption,
        ),
    ]
    return functools.reduce(lambda x, opt: opt(x), reversed(options), f)


def common_experiment_create_multi_node_options(f):
    options = [
        click.option(
            "--experimentType",
            "experiment_type_id",
            type=ChoiceType(constants.MULTI_NODE_EXPERIMENT_TYPES_MAP, case_sensitive=False),
            required=True,
            help="Experiment Type",
            cls=common.GradientOption,
        ),
        click.option(
            "--workerContainer",
            "worker_container",
            metavar="<container>",
            required=True,
            help="Worker container",
            cls=common.GradientOption,
        ),
        click.option(
            "--workerMachineType",
            "worker_machine_type",
            metavar="<machine type>",
            required=True,
            help="Worker machine type",
            cls=common.GradientOption,
        ),
        click.option(
            "--workerCommand",
            "worker_command",
            metavar="<command>",
            required=True,
            help="Worker command",
            cls=common.GradientOption,
        ),
        click.option(
            "--workerCount",
            "worker_count",
            type=int,
            required=True,
            help="Worker count",
            cls=common.GradientOption,
        ),
        click.option(
            "--parameterServerContainer",
            "parameter_server_container",
            metavar="<container>",
            help="Parameter server container (GRPC only)",
            cls=common.GradientOption,
        ),
        click.option(
            "--parameterServerMachineType",
            "parameter_server_machine_type",
            metavar="<machine type>",
            help="Parameter server machine type (GRPC only)",
            cls=common.GradientOption,
        ),
        click.option(
            "--parameterServerCommand",
            "parameter_server_command",
            metavar="<command>",
            help="Parameter server command (GRPC only)",
            cls=common.GradientOption,
        ),
        click.option(
            "--parameterServerCount",
            "parameter_server_count",
            type=int,
            help="Parameter server count (GRPC only)",
            cls=common.GradientOption,
        ),
        click.option(
            "--masterContainer",
            "master_container",
            metavar="<container>",
            help="Master container (MPI only)",
            cls=common.GradientOption,
        ),
        click.option(
            "--masterMachineType",
            "master_machine_type",
            metavar="<machine type>",
            help="Master machine type (MPI only)",
            cls=common.GradientOption,
        ),
        click.option(
            "--masterCount",
            "master_count",
            help="Master count (MPI only)",
            cls=common.GradientOption,
        ),
        click.option(
            "--masterCommand",
            "master_command",
            metavar="<command>",
            help="Master command (MPI only)",
            cls=common.GradientOption,
        ),
        click.option(
            "--workerContainerUser",
            "worker_container_user",
            help="Worker container user",
            cls=common.GradientOption,
        ),
        click.option(
            "--workerRegistryUsername",
            "worker_registry_username",
            help="Worker container registry username",
            cls=common.GradientOption,
        ),
        click.option(
            "--workerRegistryPassword",
            "worker_registry_password",
            metavar="<password>",
            help="Worker registry password",
            cls=common.GradientOption,
        ),
        click.option(
            "--workerRegistryUrl",
            "worker_registry_url",
            metavar="<registry url>",
            help="Worker registry URL",
            cls=common.GradientOption,
        ),
        click.option(
            "--parameterServerContainerUser",
            "parameter_server_container_user",
            help="Parameter server container user",
            cls=common.GradientOption,
        ),
        click.option(
            "--parameterServerRegistryUsername",
            "parameter_server_registry_username",
            help="Parameter server registry username",
            cls=common.GradientOption,
        ),
        click.option(
            "--parameterServerRegistryPassword",
            "parameter_server_registry_password",
            metavar="<password>",
            help="Parameter server registry password",
            cls=common.GradientOption,
        ),
        click.option(
            "--parameterServerRegistryUrl",
            "parameter_server_registry_url",
            metavar="<registry url>",
            help="Parameter server registry URL",
            cls=common.GradientOption,
        ),
        click.option(
            "--masterContainerUser",
            "master_container_user",
            help="Master container user (MPI only)",
            cls=common.GradientOption,
        ),
        click.option(
            "--masterRegistryUsername",
            "master_registry_username",
            metavar="<username>",
            help="Master registry username (MPI only)",
            cls=common.GradientOption,
        ),
        click.option(
            "--masterRegistryPassword",
            "master_registry_password",
            metavar="<password>",
            help="Master registry password (MPI only)",
            cls=common.GradientOption,
        ),
        click.option(
            "--masterRegistryUrl",
            "master_registry_url",
            metavar="<registry url>",
            help="Master registry URL (MPI only)",
            cls=common.GradientOption
        ),
    ]
    return functools.reduce(lambda x, opt: opt(x), reversed(options), f)


def common_experiments_create_single_node_options(f):
    options = [
        click.option(
            "--container",
            required=True,
            help="Container",
            cls=common.GradientOption,
        ),
        click.option(
            "--machineType",
            "machine_type",
            required=True,
            metavar="<machine type>",
            help="Machine type",
            cls=common.GradientOption,
        ),
        click.option(
            "--command",
            required=True,
            metavar="<command>",
            help="Container entrypoint command",
            cls=common.GradientOption,
        ),
        click.option(
            "--containerUser",
            "container_user",
            help="Container user",
            cls=common.GradientOption,
        ),
        click.option(
            "--registryUsername",
            "registry_username",
            help="Registry username",
            cls=common.GradientOption,
        ),
        click.option(
            "--registryPassword",
            "registry_password",
            metavar="<password>",
            help="Registry password",
            cls=common.GradientOption,
        ),
        click.option(
            "--registryUrl",
            "registry_url",
            metavar="<registry url>",
            help="Registry URL",
            cls=common.GradientOption,
        ),
    ]
    return functools.reduce(lambda x, opt: opt(x), reversed(options), f)


def tensorboard_option(f):
    options = [
        click.option(
            "--tensorboard",
            is_flag=True,
            # default=experiments_commands.NoTensorboardId,
            help="Creates new tensorboard for this experiment",
            cls=GradientRegisterReaderOption,
        ),
        click.option(
            "--tensorboard_set",
            help="Add to existing tensorboard",
            cls=GradientRegisterWriterOption,
            metavar='<tensorboard ID>'
        ),
    ]
    return functools.reduce(lambda x, opt: opt(x), reversed(options), f)


def parse_tensorboard_options(tensorboard, tensorboard_set):
    """
    :param str|bool tensorboard:
    :param str|None tensorboard_set:
    :rtype: str|bool
    """
    if tensorboard is True:
        return True

    if tensorboard_set:
        return tensorboard_set
    else:
        return False


@create_experiment.command(name="multinode", help="Create multi node experiment", cls=GradientRegisterWriterCommand)
@common_experiments_create_options
@common_experiment_create_multi_node_options
@dataset_options
@tensorboard_option
@api_key_option
@common.options_file
def create_multi_node(api_key, tensorboard, tensorboard_set, options_file, **kwargs):
    kwargs["tags"] = validate_comma_split_option(kwargs.pop("tags_comma"), kwargs.pop("tags"))
    add_to_tensorboard = parse_tensorboard_options(tensorboard, tensorboard_set)

    validators.validate_multi_node(kwargs)
    common.del_if_value_is_none(kwargs)
    experiment_type = kwargs.get('experiment_type_id')
    command_class = MULTI_NODE_CREATE_EXPERIMENT_COMMANDS.get(experiment_type)
    command = command_class(
        api_key=api_key,
        workspace_handler=get_workspace_handler(api_key),
    )
    command.execute(kwargs, add_to_tensorboard=add_to_tensorboard)


@create_experiment.command(name="singlenode", help="Create single node experiment", cls=GradientRegisterWriterCommand)
@common_experiments_create_options
@common_experiments_create_single_node_options
@dataset_options
@tensorboard_option
@api_key_option
@common.options_file
def create_single_node(api_key, tensorboard, tensorboard_set, options_file, **kwargs):
    kwargs["tags"] = validate_comma_split_option(kwargs.pop("tags_comma"), kwargs.pop("tags"))
    add_to_tensorboard = parse_tensorboard_options(tensorboard, tensorboard_set)

    common.del_if_value_is_none(kwargs)

    command = experiments_commands.CreateSingleNodeExperimentCommand(
        api_key=api_key,
        workspace_handler=get_workspace_handler(api_key),
    )
    command.execute(kwargs, add_to_tensorboard=add_to_tensorboard)


@create_and_start_experiment.command(name="multinode", help="Create and start new multi node experiment",
                                     cls=GradientRegisterWriterCommand)
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
@dataset_options
@tensorboard_option
@api_key_option
@common.options_file
@click.pass_context
def create_and_start_multi_node(ctx, api_key, show_logs, tensorboard, tensorboard_set, options_file, **kwargs):
    kwargs["tags"] = validate_comma_split_option(kwargs.pop("tags_comma"), kwargs.pop("tags"))
    add_to_tensorboard = parse_tensorboard_options(tensorboard, tensorboard_set)

    validators.validate_multi_node(kwargs)
    common.del_if_value_is_none(kwargs)

    experiment_type = kwargs.get('experiment_type_id')
    command_class = MULTI_NODE_RUN_EXPERIMENT_COMMANDS.get(experiment_type)

    command = command_class(
        api_key=api_key,
        workspace_handler=get_workspace_handler(api_key),
    )
    experiment_id = command.execute(kwargs, add_to_tensorboard=add_to_tensorboard)
    if experiment_id and show_logs:
        ctx.invoke(list_logs, experiment_id=experiment_id, line=1, limit=100, follow=True, api_key=api_key)


@create_and_start_experiment.command(name="singlenode", help="Create and start new single node experiment",
                                     cls=GradientRegisterWriterCommand)
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
@dataset_options
@tensorboard_option
@api_key_option
@common.options_file
@click.pass_context
def create_and_start_single_node(ctx, api_key, show_logs, tensorboard, tensorboard_set, options_file,
                                 **kwargs):
    kwargs["tags"] = validate_comma_split_option(kwargs.pop("tags_comma"), kwargs.pop("tags"))
    add_to_tensorboard = parse_tensorboard_options(tensorboard, tensorboard_set)

    common.del_if_value_is_none(kwargs)

    command = experiments_commands.CreateAndStartSingleNodeExperimentCommand(
        api_key=api_key,
        workspace_handler=get_workspace_handler(api_key),
    )
    experiment_id = command.execute(kwargs, add_to_tensorboard=add_to_tensorboard)
    if experiment_id and show_logs:
        ctx.invoke(list_logs, experiment_id=experiment_id, line=1, limit=100, follow=True, api_key=api_key)


@experiments_group.command("start", help="Start experiment")
@click.option(
    "--id",
    "id",
    required=True,
    cls=common.GradientOption,
    help="ID of the experiment",
)
@click.option(
    "--logs",
    "show_logs",
    is_flag=True,
    help="Show logs",
)
@api_key_option
@common.options_file
@click.pass_context
def start_experiment(ctx, id, show_logs, api_key, options_file):
    command = experiments_commands.StartExperimentCommand(api_key=api_key)
    command.execute(id)

    if show_logs:
        ctx.invoke(list_logs, experiment_id=id, line=1, limit=100, follow=True, api_key=api_key)


@experiments_group.command("stop", help="Stop experiment")
@click.option(
    "--id",
    "id",
    required=True,
    cls=common.GradientOption,
    help="ID of the experiment",
)
@api_key_option
@common.options_file
def stop_experiment(id, api_key, options_file):
    command = experiments_commands.StopExperimentCommand(api_key=api_key)
    command.execute(id)


@experiments_group.command("list", help="List experiments")
@click.option(
    "--projectId",
    "-p",
    "project_ids",
    multiple=True,
    metavar='<project ID>',
    help="Filter by project IDs. Multiple use",
    cls=common.GradientOption,
)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    cls=common.GradientOption,
    help="Filter by tags. Multiple use"
)
@click.option(
    "--limit",
    "-l",
    "exp_limit",
    default=20,
    help="Limit listed experiments per page",
    cls=common.GradientOption,
)
@click.option(
    "--offset",
    "-o",
    "exp_offset",
    default=0,
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def list_experiments(project_ids, api_key, exp_limit, exp_offset, tags, options_file):
    command = experiments_commands.ListExperimentsCommand(api_key=api_key)

    res = command.execute(project_id=project_ids, limit=exp_limit, offset=exp_offset, tags=tags)
    for experiments_str, next_iteration in res:
        click.echo(experiments_str)
        if next_iteration:
            click.confirm("Do you want to continue?", abort=True)


@experiments_group.command("details", help="Show detail of an experiment")
@click.option(
    "--id",
    "id",
    required=True,
    cls=common.GradientOption,
    help="ID of the experiment",
)
@api_key_option
@common.options_file
def get_experiment_details(id, options_file, api_key):
    command = experiments_commands.GetExperimentCommand(api_key=api_key)
    command.execute(id)


@experiments_group.command("logs", help="List experiment logs")
@click.option(
    "--id",
    "experiment_id",
    required=True,
    cls=common.GradientOption,
)
@click.option(
    "--line",
    "line",
    required=False,
    default=0,
    cls=common.GradientOption,
)
@click.option(
    "--limit",
    "limit",
    required=False,
    default=10000,
    cls=common.GradientOption,
)
@click.option(
    "--follow",
    "follow",
    required=False,
    default=False,
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def list_logs(experiment_id, line, limit, follow, options_file, api_key=None):
    command = experiments_commands.ExperimentLogsCommand(api_key=api_key)
    command.execute(experiment_id, line, limit, follow)


@experiments_group.command("delete", help="Delete an experiment")
@click.option(
    "--id",
    "id",
    required=True,
    cls=common.GradientOption,
    help="ID of the experiment",
)
@api_key_option
@common.options_file
def delete_experiment(id, options_file, api_key):
    command = experiments_commands.DeleteExperimentCommand(api_key=api_key)
    command.execute(id)


@experiments_tags.command("add", help="Add tags to experiment")
@click.option(
    "--id",
    "id",
    required=True,
    cls=common.GradientOption,
    help="ID of the experiment",
)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    help="One or many tags that you want to add to experiment",
    cls=common.GradientOption
)
@click.option(
    "--tags",
    "tags_comma",
    help="Separated by comma tags that you want add to experiment",
    cls=common.GradientOption
)
@api_key_option
@common.options_file
def experiment_add_tags(id, options_file, api_key, **kwargs):
    kwargs["tags"] = validate_comma_split_option(kwargs.pop("tags_comma"), kwargs.pop("tags"), raise_if_no_values=True)

    command = ExperimentAddTagsCommand(api_key=api_key)
    command.execute(id, **kwargs)


@experiments_tags.command("remove", help="Remove tags from experiment")
@click.option(
    "--id",
    "id",
    required=True,
    cls=common.GradientOption,
    help="ID of the experiment",
)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    help="One or many tags that you want to remove from experiment",
    cls=common.GradientOption
)
@click.option(
    "--tags",
    "tags_comma",
    help="Separated by comma tags that you want to remove from experiment",
    cls=common.GradientOption
)
@api_key_option
@common.options_file
def experiment_remove_tags(id, options_file, api_key, **kwargs):
    kwargs["tags"] = validate_comma_split_option(kwargs.pop("tags_comma"), kwargs.pop("tags"), raise_if_no_values=True)

    command = ExperimentRemoveTagsCommand(api_key=api_key)
    command.execute(id, **kwargs)


@experiments_metrics.command(
    "get",
    short_help="Get experiment metrics",
    help="Get experiment metrics. Shows CPU and RAM usage by default",
)
@click.option(
    "--id",
    "experiment_id",
    required=True,
    cls=common.GradientOption,
    help="ID of the experiment",
)
@click.option(
    "--metric",
    "metrics_list",
    multiple=True,
    type=ChoiceType(constants.METRICS_MAP, case_sensitive=False),
    default=(constants.BuiltinMetrics.cpu_percentage, constants.BuiltinMetrics.memory_usage),
    help="One or more metrics that you want to read. Defaults to cpuPercentage and memoryUsage",
    cls=common.GradientOption,
)
@click.option(
    "--interval",
    "interval",
    default="30s",
    help="Interval",
    cls=common.GradientOption,
)
@click.option(
    "--start",
    "start",
    type=click.DateTime(),
    help="Timestamp of first time series metric to collect",
    cls=common.GradientOption,
)
@click.option(
    "--end",
    "end",
    type=click.DateTime(),
    help="Timestamp of last time series metric to collect",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def get_experiment_metrics(experiment_id, metrics_list, interval, start, end, options_file, api_key):
    command = GetExperimentMetricsCommand(api_key=api_key)
    command.execute(experiment_id, start, end, interval, built_in_metrics=metrics_list)


@experiments_metrics.command(
    "stream",
    short_help="Watch live experiment metrics",
    help="Watch live experiment metrics. Shows CPU and RAM usage by default",
)
@click.option(
    "--id",
    "experiment_id",
    required=True,
    cls=common.GradientOption,
    help="ID of the experiment",
)
@click.option(
    "--metric",
    "metrics_list",
    multiple=True,
    type=ChoiceType(constants.METRICS_MAP, case_sensitive=False),
    default=(constants.BuiltinMetrics.cpu_percentage, constants.BuiltinMetrics.memory_usage),
    help="One or more metrics that you want to read. Defaults to cpuPercentage and memoryUsage",
    cls=common.GradientOption,
)
@click.option(
    "--interval",
    "interval",
    default="30s",
    help="Interval",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def get_experiment_metrics_stream(experiment_id, metrics_list, interval, options_file, api_key):
    command = StreamExperimentMetricsCommand(api_key=api_key)
    command.execute(experiment_id=experiment_id, interval=interval, built_in_metrics=metrics_list)
