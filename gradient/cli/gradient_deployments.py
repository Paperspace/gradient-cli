import click
import logging
import os
import json
import yaml
from gql import gql
from gql.transport.exceptions import TransportQueryError

from gradient.api_sdk.repositories import gradient_deployments
from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.common import api_key_option, ClickGroup
from gradient.commands.helpers import print_table, formatted_graphql
from gradient.exceptions import ApplicationError


logger = logging.getLogger(__name__)


def load_spec(spec_path):
    if not os.path.exists(spec_path):
        raise ApplicationError(
            'Source path not found: {}'.format(spec_path))
    yaml_spec = open(spec_path, 'r')
    return yaml.safe_load(yaml_spec)


@cli.group("deployments", help="Manage Deployments", cls=ClickGroup)
def deployments():
    pass


@deployments.command("create", help="Create a deployment")
@click.option(
    "--name",
    "name",
    required=True,
    help="Name",
    cls=common.GradientOption,
)
@click.option(
    "--projectId",
    "project_id",
    required=True,
    help="Project ID",
    cls=common.GradientOption,
)
@click.option(
    "--clusterId",
    "cluster_id",
    required=False,
    help="Cluster ID",
    cls=common.GradientOption,
)
@click.option(
    "--spec",
    "spec_path",
    required=True,
    help="Path to a deployment spec file",
    cls=common.GradientOption,
)
@api_key_option
@click.pass_context
def create_deployment_command(ctx, api_key, name, project_id, cluster_id, spec_path):
    try:
        spec = load_spec(spec_path)
    except Exception as error:
        logger.error(f'Invalid spec: {error}')
        return

    try:
        deployment = gradient_deployments.create_deployment(name, project_id, spec, cluster_id, api_key=api_key)
        print(f'Created deployment: {deployment["id"]}')
    except TransportQueryError as error:
        logger.error(error.errors[0]['message'])
    except Exception as error:
        logger.error(f'There was an error, please try again')


@deployments.command("update", help="Update a deployment")
@click.option(
    "--id",
    "id",
    required=True,
    help="ID",
    cls=common.GradientOption,
)
@click.option(
    "--name",
    "name",
    required=False,
    help="Name",
    cls=common.GradientOption,
)
@click.option(
    "--projectId",
    "project_id",
    required=False,
    help="Project ID",
    cls=common.GradientOption,
)
@click.option(
    "--clusterId",
    "cluster_id",
    required=False,
    help="Cluster ID",
    cls=common.GradientOption,
)
@click.option(
    "--spec",
    "spec_path",
    required=False,
    help="Path to a deployment spec file",
    cls=common.GradientOption,
)
@api_key_option
@click.pass_context
def update_deployment_command(ctx, api_key, id, name, project_id, spec_path, cluster_id):
    spec = None
    if spec_path is not None:
        try:
            spec = load_spec(spec_path)
        except Exception as error:
            logger.error(f'Invalid spec: {error}')
            return

    try:
        deployment = gradient_deployments.update_deployment(id, name, project_id, spec, cluster_id, api_key=api_key)
        print(f'Updated deployment: {deployment["id"]}')
    except TransportQueryError as error:
        logger.error(error.errors[0]['message'])
    except Exception as error:
        print(error)
        logger.error(f'There was an error, please try again')


@deployments.command("list", help="List deployments")
@click.option(
    "--name",
    "name",
    required=False,
    help="Name",
    cls=common.GradientOption,
)
@click.option(
    "--projectId",
    "project_id",
    required=False,
    help="Project ID",
    cls=common.GradientOption,
)
@click.option(
    "--clusterId",
    "cluster_id",
    required=False,
    help="Cluster ID",
    cls=common.GradientOption,
)
@api_key_option
@click.pass_context
def list_deployments_command(ctx, name, project_id, cluster_id, api_key):
    try:
        deployments = gradient_deployments.list_deployments(
            name,
            project_id,
            cluster_id,
            api_key=api_key)
        if len(deployments) == 0:
            print('No deployments found')
            return
        table_data = [('Name', 'ID')]
        for deployment in deployments:
            table_data.append((deployment['name'], deployment['id']))

        print_table(table_data)
    except TransportQueryError as error:
        logger.error(error.errors[0]['message'])
    except Exception as error:
        print(error)
        logger.error(f'There was an error, please try again')


@click.option(
    "--id",
    "id",
    required=True,
    help="ID",
    cls=common.GradientOption,
)
@deployments.command("get", help="Get a deployment")
@api_key_option
@click.pass_context
def get_deployment_command(ctx, api_key, id):
    try:
        deployment = gradient_deployments.get_deployment(id, api_key=api_key)
        if deployment['deployment'] is None:
            print('Deployment not found')
        else:
            print(json.dumps(formatted_graphql(
                deployment['deployment']), indent=4))
    except TransportQueryError as error:
        logger.error(error.errors[0]['message'])
    except Exception as error:
        print(error)
        logger.error(f'There was an error, please try again')


@click.option(
    "--id",
    "id",
    required=True,
    help="ID",
    cls=common.GradientOption,
)
@deployments.command("delete", help="Delete a deployment")
@api_key_option
@click.pass_context
def delete_deployment_command(ctx, api_key, id):
    try:
        deployment = gradient_deployments.delete_deployment(id, api_key=api_key)
        if deployment is None:
            print('Deployment not found')
        else:
            print(f'Deleted deployment: {deployment["deployment"]["id"]}')
    except TransportQueryError as error:
        logger.error(error.errors[0]['message'])
    except Exception as error:
        print(error)
        logger.error(f'There was an error, please try again')
