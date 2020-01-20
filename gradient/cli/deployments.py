import collections

import click

from gradient import exceptions, logger, DEPLOYMENT_TYPES_MAP
from gradient import utils
from gradient.api_sdk import DeploymentsClient
from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.cli_types import ChoiceType, json_string
from gradient.cli.common import api_key_option, del_if_value_is_none, ClickGroup
from gradient.commands import deployments as deployments_commands


@cli.group("deployments", help="Manage deployments", cls=ClickGroup)
def deployments():
    pass


def get_deployment_client(api_key):
    deployment_client = DeploymentsClient(api_key=api_key, logger=logger.Logger())
    return deployment_client


@deployments.command("create", help="Create new deployment")
@click.option(
    "--deploymentType",
    "deployment_type",
    type=ChoiceType(DEPLOYMENT_TYPES_MAP, case_sensitive=False),
    required=True,
    help="Model deployment type",
    cls=common.GradientOption,
)
@click.option(
    "--modelId",
    "model_id",
    required=True,
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
    "--endpointUrlPath",
    "endpoint_url_path",
    help="Endpoint URL path",
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
    "--vpc",
    "use_vpc",
    type=bool,
    is_flag=True,
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def create_deployment(api_key, use_vpc, options_file, **kwargs):
    utils.validate_auth_options(kwargs)

    del_if_value_is_none(kwargs)
    deployment_client = get_deployment_client(api_key)
    command = deployments_commands.CreateDeploymentCommand(deployment_client=deployment_client)
    command.execute(use_vpc=use_vpc, **kwargs)


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


@deployments.command("list", help="List deployments with optional filtering")
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
@api_key_option
@common.options_file
def get_deployments_list(api_key, options_file, **filters):
    del_if_value_is_none(filters)
    deployment_client = get_deployment_client(api_key)
    command = deployments_commands.ListDeploymentsCommand(deployment_client=deployment_client)
    try:
        command.execute(**filters)
    except exceptions.ApplicationError as e:
        logger.Logger().error(e)


@deployments.command("start", help="Start deployment")
@click.option(
    "--id",
    "id_",
    required=True,
    help="Deployment ID",
    cls=common.GradientOption,
)
@click.option(
    "--vpc",
    "use_vpc",
    type=bool,
    is_flag=True,
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def start_deployment(id_, use_vpc, options_file, api_key=None):
    deployment_client = get_deployment_client(api_key)
    command = deployments_commands.StartDeploymentCommand(deployment_client=deployment_client)
    command.execute(deployment_id=id_, use_vpc=use_vpc)


@deployments.command("stop", help="Stop deployment")
@click.option(
    "--id",
    "id_",
    required=True,
    help="Deployment ID",
    cls=common.GradientOption,
)
@click.option(
    "--vpc",
    "use_vpc",
    type=bool,
    is_flag=True,
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def stop_deployment(id_, use_vpc, options_file, api_key=None):
    deployment_client = get_deployment_client(api_key)
    command = deployments_commands.StopDeploymentCommand(deployment_client=deployment_client)
    command.execute(deployment_id=id_, use_vpc=use_vpc)


@deployments.command("delete", help="Delete deployment")
@click.option(
    "--id",
    "id_",
    required=True,
    help="Deployment ID",
    cls=common.GradientOption,
)
@click.option(
    "--vpc",
    "use_vpc",
    type=bool,
    is_flag=True,
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def delete_deployment(id_, use_vpc, options_file, api_key):
    deployment_client = get_deployment_client(api_key)
    command = deployments_commands.DeleteDeploymentCommand(deployment_client=deployment_client)
    command.execute(deployment_id=id_, use_vpc=use_vpc)


@deployments.command("update", help="Modify existing deployment")
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
    "--endpointUrlPath",
    "endpoint_url_path",
    help="Endpoint URL path",
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
    "--vpc",
    "use_vpc",
    type=bool,
    is_flag=True,
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def update_deployment(deployment_id, api_key, use_vpc, options_file, **kwargs):
    del_if_value_is_none(kwargs)
    deployment_client = get_deployment_client(api_key)
    command = deployments_commands.UpdateDeploymentCommand(deployment_client=deployment_client)
    command.execute(deployment_id, use_vpc=use_vpc, **kwargs)


@deployments.command("details", help="Get details of model deployment")
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
    deployment_client = get_deployment_client(api_key)
    command = deployments_commands.GetDeploymentDetails(deployment_client=deployment_client)
    command.execute(deployment_id)
