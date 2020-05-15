import collections

import click

from gradient import cliutils
from gradient import exceptions, clilogger, DEPLOYMENT_TYPES_MAP
from gradient.api_sdk import constants, workspace
from gradient.api_sdk.s3_uploader import DeploymentWorkspaceDirectoryUploader
from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.cli_types import ChoiceType, json_string
from gradient.cli.common import api_key_option, del_if_value_is_none, ClickGroup, validate_comma_split_option
from gradient.cli_constants import CLI_PS_CLIENT_NAME
from gradient.commands import deployments as deployments_commands
from gradient.commands.deployments import DeploymentRemoveTagsCommand, DeploymentAddTagsCommand, \
    GetDeploymentMetricsCommand, StreamDeploymentMetricsCommand, DeploymentLogsCommand


def get_workspace_handler(api_key):
    logger_ = clilogger.CliLogger()
    workspace_handler = workspace.S3WorkspaceHandlerWithProgressbar(api_key=api_key,
                                                                    logger_=logger_,
                                                                    uploader_cls=DeploymentWorkspaceDirectoryUploader,
                                                                    client_name=CLI_PS_CLIENT_NAME)
    return workspace_handler


@cli.group("deployments", help="Manage deployments", cls=ClickGroup)
def deployments_group():
    pass


@deployments_group.group("tags", help="Manage deployments tags", cls=ClickGroup)
def deployments_tags():
    pass


@deployments_group.group(name="metrics", help="Read model deployment metrics", cls=ClickGroup)
def deployments_metrics():
    pass


@deployments_group.command("create", help="Create new deployment")
@click.option(
    "--deploymentType",
    "deployment_type",
    type=ChoiceType(DEPLOYMENT_TYPES_MAP, case_sensitive=False),
    required=True,
    help="Model deployment type",
    cls=common.GradientOption,
)
@click.option(
    "--projectId",
    "project_id",
    help="Project ID",
    cls=common.GradientOption,
)
@click.option(
    "--modelId",
    "model_id",
    help="ID of a trained model",
    cls=common.GradientOption,
)
@click.option(
    "--name",
    "name",
    required=True,
    help="Human-friendly name for new model deployment",
    cls=common.GradientOption,
)
@click.option(
    "--machineType",
    "machine_type",
    required=True,
    help="Type of machine for new deployment",
    cls=common.GradientOption,
)
@click.option(
    "--imageUrl",
    "image_url",
    required=True,
    help="Docker image for model serving",
    cls=common.GradientOption,
)
@click.option(
    "--instanceCount",
    "instance_count",
    type=int,
    required=True,
    help="Number of machine instances",
    cls=common.GradientOption,
)
@click.option(
    "--command",
    "command",
    help="Deployment command",
    cls=common.GradientOption,
)
@click.option(
    "--containerModelPath",
    "container_model_path",
    help="Container model path",
    cls=common.GradientOption,
)
@click.option(
    "--imageUsername",
    "image_username",
    help="Username used to access docker image",
    cls=common.GradientOption,
)
@click.option(
    "--imagePassword",
    "image_password",
    help="Password used to access docker image",
    cls=common.GradientOption,
)
@click.option(
    "--imageServer",
    "image_server",
    help="Docker image server",
    cls=common.GradientOption,
)
@click.option(
    "--containerUrlPath",
    "container_url_path",
    help="Container URL path",
    cls=common.GradientOption,
)
@click.option(
    "--method",
    "method",
    help="Method",
    cls=common.GradientOption,
)
@click.option(
    "--dockerArgs",
    "docker_args",
    type=json_string,
    help="JSON-style list of docker args",
    cls=common.GradientOption,
)
@click.option(
    "--env",
    "env",
    type=json_string,
    help="JSON-style environmental variables map",
    cls=common.GradientOption,
)
@click.option(
    "--apiType",
    "api_type",
    help="Type of API",
    cls=common.GradientOption,
)
@click.option(
    "--ports",
    "ports",
    help="Ports",
    cls=common.GradientOption,
)
@click.option(
    "--clusterId",
    "cluster_id",
    help="Cluster ID",
    cls=common.GradientOption,
)
@click.option(
    "--authUsername",
    "auth_username",
    help="Username",
    cls=common.GradientOption,
)
@click.option(
    "--authPassword",
    "auth_password",
    help="Password",
    cls=common.GradientOption,
)
@click.option(
    "--auth",
    "generate_auth",
    is_flag=True,
    help="Generate username and password. Mutually exclusive with --authUsername and --authPassword",
    cls=common.GradientOption,
)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    help="One or many tags that you want to add to model deployment job",
    cls=common.GradientOption
)
@click.option(
    "--tags",
    "tags_comma",
    help="Separated by comma tags that you want add to model deployment job",
    cls=common.GradientOption
)
@click.option(
    "--workspace",
    "workspace",
    help="Path to workspace directory, archive, S3 or git repository",
    default="none",
    cls=common.GradientOption,
)
@click.option(
    "--workspaceRef",
    "workspace_ref",
    help="Git commit hash, branch name or tag",
    cls=common.GradientOption,
)
@click.option(
    "--workspaceUsername",
    "workspace_username",
    help="Workspace username",
    cls=common.GradientOption,
)
@click.option(
    "--workspacePassword",
    "workspace_password",
    help="Workspace password",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def create_deployment(api_key, options_file, **kwargs):
    cliutils.validate_auth_options(kwargs)
    kwargs["tags"] = validate_comma_split_option(kwargs.pop("tags_comma"), kwargs.pop("tags"))
    del_if_value_is_none(kwargs)
    command = deployments_commands.CreateDeploymentCommand(api_key=api_key,
                                                           workspace_handler=get_workspace_handler(api_key))
    command.execute(**kwargs)


DEPLOYMENT_STATES_MAP = collections.OrderedDict(
    (
        ("BUILDING", "Building"),
        ("PROVISIONING", "Provisioning"),
        ("STARTING", "Starting"),
        ("RUNNING", "Running"),
        ("STOPPING", "Stopping"),
        ("STOPPED", "Stopped"),
        ("ERROR", "Error"),
    )
)


@deployments_group.command("list", help="List deployments with optional filtering")
@click.option(
    "--state",
    "state",
    type=ChoiceType(DEPLOYMENT_STATES_MAP, case_sensitive=False),
    help="Filter by deployment state",
    cls=common.GradientOption,
)
@click.option(
    "--projectId",
    "project_id",
    help="Use to filter by project ID",
    cls=common.GradientOption,
)
@click.option(
    "--modelId",
    "model_id",
    help="Use to filter by model ID",
    cls=common.GradientOption,
)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    cls=common.GradientOption,
    help="Filter by tags. Multiple use"
)
@api_key_option
@common.options_file
def get_deployments_list(api_key, options_file, **filters):
    del_if_value_is_none(filters)
    command = deployments_commands.ListDeploymentsCommand(api_key=api_key)
    try:
        command.execute(**filters)
    except exceptions.ApplicationError as e:
        clilogger.CliLogger().error(e)


@deployments_group.command("start", help="Start deployment")
@click.option(
    "--id",
    "id_",
    required=True,
    help="Deployment ID",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def start_deployment(id_, options_file, api_key=None):
    command = deployments_commands.StartDeploymentCommand(api_key=api_key)
    command.execute(deployment_id=id_)


@deployments_group.command("stop", help="Stop deployment")
@click.option(
    "--id",
    "id_",
    required=True,
    help="Deployment ID",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def stop_deployment(id_, options_file, api_key=None):
    command = deployments_commands.StopDeploymentCommand(api_key=api_key)
    command.execute(deployment_id=id_)


@deployments_group.command("delete", help="Delete deployment")
@click.option(
    "--id",
    "id_",
    required=True,
    help="Deployment ID",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def delete_deployment(id_, options_file, api_key):
    command = deployments_commands.DeleteDeploymentCommand(api_key=api_key)
    command.execute(deployment_id=id_)


@deployments_group.command("update", help="Modify existing deployment")
@click.option(
    "--id",
    "deployment_id",
    required=True,
    help="ID of existing deployment",
    cls=common.GradientOption,
)
@click.option(
    "--deploymentType",
    "deployment_type",
    type=ChoiceType(DEPLOYMENT_TYPES_MAP, case_sensitive=False),
    help="Model deployment type",
    cls=common.GradientOption,
)
@click.option(
    "--projectId",
    "project_id",
    help="Project ID",
    cls=common.GradientOption,
)
@click.option(
    "--modelId",
    "model_id",
    help="ID of a trained model",
    cls=common.GradientOption,
)
@click.option(
    "--name",
    "name",
    help="Human-friendly name for new model deployment",
    cls=common.GradientOption,
)
@click.option(
    "--machineType",
    "machine_type",
    help="Type of machine for new deployment",
    cls=common.GradientOption,
)
@click.option(
    "--imageUrl",
    "image_url",
    help="Docker image for model serving",
    cls=common.GradientOption,
)
@click.option(
    "--instanceCount",
    "instance_count",
    type=int,
    help="Number of machine instances",
    cls=common.GradientOption,
)
@click.option(
    "--command",
    "command",
    help="Deployment command",
    cls=common.GradientOption,
)
@click.option(
    "--containerModelPath",
    "container_model_path",
    help="Container model path",
    cls=common.GradientOption,
)
@click.option(
    "--imageUsername",
    "image_username",
    help="Username used to access docker image",
    cls=common.GradientOption,
)
@click.option(
    "--imagePassword",
    "image_password",
    help="Password used to access docker image",
    cls=common.GradientOption,
)
@click.option(
    "--imageServer",
    "image_server",
    help="Docker image server",
    cls=common.GradientOption,
)
@click.option(
    "--containerUrlPath",
    "container_url_path",
    help="Container URL path",
    cls=common.GradientOption,
)
@click.option(
    "--method",
    "method",
    help="Method",
    cls=common.GradientOption,
)
@click.option(
    "--dockerArgs",
    "docker_args",
    type=json_string,
    help="JSON-style list of docker args",
    cls=common.GradientOption,
)
@click.option(
    "--env",
    "env",
    type=json_string,
    help="JSON-style environmental variables map",
    cls=common.GradientOption,
)
@click.option(
    "--apiType",
    "api_type",
    help="Type of API",
    cls=common.GradientOption,
)
@click.option(
    "--ports",
    "ports",
    help="Ports",
    cls=common.GradientOption,
)
@click.option(
    "--authUsername",
    "auth_username",
    help="Username",
    cls=common.GradientOption,
)
@click.option(
    "--authPassword",
    "auth_password",
    help="Password",
    cls=common.GradientOption,
)
@click.option(
    "--clusterId",
    "cluster_id",
    help="Cluster ID",
    cls=common.GradientOption,
)
@click.option(
    "--workspace",
    "workspace",
    help="Path to workspace directory, archive, S3 or git repository",
    default="none",
    cls=common.GradientOption,
)
@click.option(
    "--workspaceRef",
    "workspace_ref",
    help="Git commit hash, branch name or tag",
    cls=common.GradientOption,
)
@click.option(
    "--workspaceUsername",
    "workspace_username",
    metavar="<username>",
    help="Workspace username",
    cls=common.GradientOption,
)
@click.option(
    "--workspacePassword",
    "workspace_password",
    help="Workspace password",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def update_deployment(deployment_id, api_key, options_file, **kwargs):
    del_if_value_is_none(kwargs)
    command = deployments_commands.UpdateDeploymentCommand(api_key=api_key,
                                                           workspace_handler=get_workspace_handler(api_key))
    command.execute(deployment_id, **kwargs)


@deployments_group.command("details", help="Get details of model deployment")
@click.option(
    "--id",
    "deployment_id",
    required=True,
    help="Deployment ID",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def get_deployment(deployment_id, api_key, options_file):
    command = deployments_commands.GetDeploymentDetails(api_key=api_key)
    command.execute(deployment_id)


@deployments_tags.command("add", help="Add tags to deployment")
@click.option(
    "--id",
    "id",
    required=True,
    cls=common.GradientOption,
    help="ID of the deployment",
)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    help="One or many tags that you want to add to deployment",
    cls=common.GradientOption
)
@click.option(
    "--tags",
    "tags_comma",
    help="Separated by comma tags that you want add to deployment",
    cls=common.GradientOption
)
@api_key_option
@common.options_file
def deployment_add_tag(id, options_file, api_key, **kwargs):
    kwargs["tags"] = validate_comma_split_option(kwargs.pop("tags_comma"), kwargs.pop("tags"), raise_if_no_values=True)

    command = DeploymentAddTagsCommand(api_key=api_key)
    command.execute(id, **kwargs)


@deployments_tags.command("remove", help="Remove tags from deployment")
@click.option(
    "--id",
    "id",
    required=True,
    cls=common.GradientOption,
    help="ID of the deployment",
)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    help="One or many tags that you want to remove from deployment",
    cls=common.GradientOption
)
@click.option(
    "--tags",
    "tags_comma",
    help="Separated by comma tags that you want to remove from deployment",
    cls=common.GradientOption
)
@api_key_option
@common.options_file
def deployment_remove_tags(id, options_file, api_key, **kwargs):
    kwargs["tags"] = validate_comma_split_option(kwargs.pop("tags_comma"), kwargs.pop("tags"), raise_if_no_values=True)

    command = DeploymentRemoveTagsCommand(api_key=api_key)
    command.execute(id, **kwargs)


@deployments_metrics.command(
    "get",
    short_help="Get model deployment metrics",
    help="Get model deployment metrics. Shows CPU and RAM usage by default",
)
@click.option(
    "--id",
    "deployment_id",
    required=True,
    cls=common.GradientOption,
    help="ID of the model deployment",
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
def get_deployment_metrics(deployment_id, metrics_list, interval, start, end, options_file, api_key):
    command = GetDeploymentMetricsCommand(api_key=api_key)
    command.execute(deployment_id, start, end, interval, built_in_metrics=metrics_list)


@deployments_metrics.command(
    "stream",
    short_help="Watch live model deployment metrics",
    help="Watch live model deployment metrics. Shows CPU and RAM usage by default",
)
@click.option(
    "--id",
    "deployment_id",
    required=True,
    cls=common.GradientOption,
    help="ID of the model deployment",
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
def stream_model_deployment_metrics(deployment_id, metrics_list, interval, options_file, api_key):
    command = StreamDeploymentMetricsCommand(api_key=api_key)
    command.execute(deployment_id=deployment_id, interval=interval, built_in_metrics=metrics_list)


@deployments_group.command("logs", help="List deployment logs")
@click.option(
    "--id",
    "deployment_id",
    required=True,
    cls=common.GradientOption,
)
@click.option(
    "--line",
    "line",
    default=0,
    cls=common.GradientOption,
)
@click.option(
    "--limit",
    "limit",
    default=10000,
    cls=common.GradientOption,
)
@click.option(
    "--follow",
    "follow",
    default=False,
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def list_logs(deployment_id, line, limit, follow, options_file, api_key=None):
    command = DeploymentLogsCommand(api_key=api_key)
    command.execute(deployment_id, line, limit, follow)
