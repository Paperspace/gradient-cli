import collections

import click

from gradient import exceptions, logger
from gradient.api_sdk import DeploymentsClient
from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.cli_types import ChoiceType
from gradient.cli.common import api_key_option, del_if_value_is_none, ClickGroup
from gradient.commands import deployments as deployments_commands


@cli.group("deployments", help="Manage deployments", cls=ClickGroup)
def deployments():
    pass


DEPLOYMENT_TYPES_MAP = collections.OrderedDict(
    (
        ("TFSERVING", "Tensorflow Serving on K8s"),
        # ("GRADIENT", "Gradient Jobs"),
    )
)

DEPLOYMENT_MACHINE_TYPES = (
    "G1", "G6", "G12",
    "K80", "P100", "GV100",
    # VPC machine types
    "c5.xlarge", "c5.4xlarge", "c5.12xlarge",
    "p2.xlarge", "p3.2xlarge", "p3.16xlarge",
)


def get_deployment_client(api_key):
    deployment_client = DeploymentsClient(api_key=api_key, logger=logger.Logger())
    return deployment_client


@deployments.command("create", help="Create new deployment")
@click.option(
    "--deploymentType",
    "deployment_type",
    type=ChoiceType(DEPLOYMENT_TYPES_MAP, case_sensitive=False),
    required=True,
    help="Model deployment type. Only TensorFlow models can currently be deployed",
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
def create_deployment(api_key, use_vpc, options_file, **kwargs):
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
