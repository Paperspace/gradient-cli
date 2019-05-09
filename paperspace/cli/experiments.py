import collections
import functools

import click

from paperspace import client, config, constants
from paperspace.cli.cli import cli
from paperspace.cli.cli_types import json_string, ChoiceType
from paperspace.cli.common import api_key_option, del_if_value_is_none, ClickGroup
from paperspace.commands import experiments as experiments_commands

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


@experiments.group(name="createAndStart", help="Create and start new experiment", cls=ClickGroup)
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
            "--experimentTypeId",
            "experimentTypeId",
            type=ChoiceType(MULTI_NODE_EXPERIMENT_TYPES_MAP, case_sensitive=False),
            required=True,
            help="Experiment Type ID",
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


@create_experiment.command(name="multinode", help="Create multi node experiment")
@common_experiments_create_options
@common_experiment_create_multi_node_options
def create_multi_node(api_key, **kwargs):
    del_if_value_is_none(kwargs)
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    command = experiments_commands.CreateExperimentCommand(api=experiments_api)
    command.execute(kwargs)


@create_experiment.command(name="singlenode", help="Create single node experiment")
@common_experiments_create_options
@common_experiments_create_single_node_options
def create_single_node(api_key, **kwargs):
    kwargs["experimentTypeId"] = constants.ExperimentType.SINGLE_NODE
    del_if_value_is_none(kwargs)
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    command = experiments_commands.CreateExperimentCommand(api=experiments_api)
    command.execute(kwargs)


@create_and_start_experiment.command(name="multinode", help="Create and start new multi node experiment")
@common_experiments_create_options
@common_experiment_create_multi_node_options
def create_and_start_multi_node(api_key, **kwargs):
    del_if_value_is_none(kwargs)
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    command = experiments_commands.CreateAndStartExperimentCommand(api=experiments_api)
    command.execute(kwargs)


@create_and_start_experiment.command(name="singlenode", help="Create and start new single node experiment")
@common_experiments_create_options
@common_experiments_create_single_node_options
def create_and_start_single_node(api_key, **kwargs):
    kwargs["experimentTypeId"] = constants.ExperimentType.SINGLE_NODE
    del_if_value_is_none(kwargs)
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    command = experiments_commands.CreateAndStartExperimentCommand(api=experiments_api)
    command.execute(kwargs)


@experiments.command("start", help="Start experiment")
@click.argument("experiment-id")
@api_key_option
def start_experiment(experiment_id, api_key):
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    experiments_commands.start_experiment(experiment_id, api=experiments_api)


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
