import collections
import functools
import json

import click

from paperspace import constants
from paperspace.commands import experiments as experiments_commands, deployments as deployments_commands


class ChoiceType(click.Choice):
    """Takes a string-keyed map and converts cli-provided parameter to corresponding value"""

    def __init__(self, type_map, case_sensitive=True):
        super(ChoiceType, self).__init__(tuple(type_map.keys()), case_sensitive=case_sensitive)
        self.type_map = type_map

    def convert(self, value, param, ctx):
        value = super(ChoiceType, self).convert(value, param, ctx).upper()
        return self.type_map[value]


MULTI_NODE_EXPERIMENT_TYPES_MAP = collections.OrderedDict(
    (
        ("GRPC", constants.ExperimentType.GRPC_MULTI_NODE),
        ("MPI", constants.ExperimentType.MPI_MULTI_NODE),
    )
)


def json_string(val):
    """Wraps json.loads so the cli help shows proper option's type name instead of 'LOADS'"""
    return json.loads(val)


def del_if_value_is_none(dict_):
    """Remove all elements with value == None"""
    for key, val in list(dict_.items()):
        if val is None:
            del dict_[key]


@click.group()
def cli():
    pass


@cli.group("experiments")
def experiments():
    pass


@experiments.group()
def create():
    pass


@experiments.group(name="createAndStart")
def create_and_start():
    pass


def common_experiments_create_options(f):
    options = [
        click.option(
            "--name",
            required=True,
        ),
        click.option(
            "--ports",
            type=int,
        ),
        click.option(
            "--workspaceUrl",
            "workspaceUrl",
            required=True,
        ),
        click.option(
            "--workingDirectory",
            "workingDirectory",
        ),
        click.option(
            "--artifactDirectory",
            "artifactDirectory",
        ),
        click.option(
            "--clusterId",
            "clusterId",
            type=int,
        ),
        click.option(
            "--experimentEnv",
            "experimentEnv",
            type=json_string,
        ),
        click.option(
            "--triggerEventId",
            "triggerEventId",
            type=int,
        ),
        click.option(
            "--projectId",
            "projectId",
            type=int,
        ),
        click.option(
            "--projectHandle",
            "projectHandle",
            required=True,
        ),
        click.option(
            "--modelType",
            "modelType",
        ),
        click.option(
            "--modelPath",
            "modelPath",
        ),
    ]
    return functools.reduce(lambda x, opt: opt(x), reversed(options), f)


def common_experiment_create_multi_node_options(f):
    options = [
        click.option(
            "--experimentTypeId",
            "experimentTypeId",
            type=ChoiceType(MULTI_NODE_EXPERIMENT_TYPES_MAP, case_sensitive=False),
            required=True,
        ),
        click.option(
            "--workerContainer",
            "workerContainer",
            required=True,
        ),
        click.option(
            "--workerMachineType",
            "workerMachineType",
            required=True,
        ),
        click.option(
            "--workerCommand",
            "workerCommand",
            required=True,
        ),
        click.option(
            "--workerCount",
            "workerCount",
            type=int,
            required=True,
        ),
        click.option(
            "--parameterServerContainer",
            "parameterServerContainer",
            required=True,
        ),
        click.option(
            "--parameterServerMachineType",
            "parameterServerMachineType",
            required=True,
        ),
        click.option(
            "--parameterServerCommand",
            "parameterServerCommand",
            required=True,
        ),
        click.option(
            "--parameterServerCount",
            "parameterServerCount",
            type=int,
            required=True,
        ),
        click.option(
            "--workerContainerUser",
            "workerContainerUser",
        ),
        click.option(
            "--workerRegistryUsername",
            "workerRegistryUsername",
        ),
        click.option(
            "--workerRegistryPassword",
            "workerRegistryPassword",
        ),
        click.option(
            "--parameterServerContainerUser",
            "parameterServerContainerUser",
        ),
        click.option(
            "--parameterServerRegistryContainerUser",
            "parameterServerRegistryContainerUser",
        ),
        click.option(
            "--parameterServerRegistryPassword",
            "parameterServerRegistryPassword",
        ),
    ]
    return functools.reduce(lambda x, opt: opt(x), reversed(options), f)


def common_experiments_create_single_node_options(f):
    options = [
        click.option(
            "--container",
            required=True,
        ),
        click.option(
            "--machineType",
            "machineType",
            required=True,
        ),
        click.option(
            "--command",
            required=True,
        ),
        click.option(
            "--containerUser",
            "containerUser",
        ),
        click.option(
            "--registryUsername",
            "registryUsername",
        ),
        click.option(
            "--registryPassword",
            "registryPassword",
        ),
    ]
    return functools.reduce(lambda x, opt: opt(x), reversed(options), f)


@create.command(name="multinode")
@common_experiments_create_options
@common_experiment_create_multi_node_options
def create_multi_node(**kwargs):
    del_if_value_is_none(kwargs)
    experiments_commands.create_experiment(kwargs)


@create.command(name="singlenode")
@common_experiments_create_options
@common_experiments_create_single_node_options
def create_single_node(**kwargs):
    kwargs["experimentTypeId"] = constants.ExperimentType.SINGLE_NODE
    del_if_value_is_none(kwargs)
    experiments_commands.create_experiment(kwargs)


@create_and_start.command(name="multinode")
@common_experiments_create_options
@common_experiment_create_multi_node_options
def create_and_start_multi_node(**kwargs):
    del_if_value_is_none(kwargs)
    experiments_commands.create_and_start_experiment(kwargs)


@create_and_start.command(name="singlenode")
@common_experiments_create_options
@common_experiments_create_single_node_options
def create_and_start_single_node(**kwargs):
    kwargs["experimentTypeId"] = constants.ExperimentType.SINGLE_NODE
    del_if_value_is_none(kwargs)
    experiments_commands.create_and_start_experiment(kwargs)


@experiments.command()
@click.argument("experiment-handle")
def start(experiment_handle):
    experiments_commands.start_experiment(experiment_handle)


@experiments.command()
@click.argument("experiment-handle")
def stop(experiment_handle):
    experiments_commands.stop_experiment(experiment_handle)


@experiments.command("list")
@click.option("--projectHandle", "-p", "project_handles", multiple=True)
def list_experiments(project_handles):
    command = experiments_commands.ListExperimentsCommand()
    command.execute(project_handles)


@experiments.command("details")
@click.argument("experiment-handle")
def get_experiment_details(experiment_handle):
    experiments_commands.get_experiment_details(experiment_handle)


# TODO: delete experiment - not implemented in the api
# TODO: modify experiment - not implemented in the api
# TODO: create experiment template?? What is the difference between experiment and experiment template?


DEPLOYMENT_TYPES_MAP = collections.OrderedDict(
    (
        ("TFSERVING", "Tensorflow Serving on K8s"),
        ("GRADIENT", "Gradient Jobs"),
    )
)


@cli.group("deployments")
def deployments():
    pass


@deployments.command("create")
@click.option(
    "--deploymentType",
    "deploymentType",
    type=ChoiceType(DEPLOYMENT_TYPES_MAP, case_sensitive=False),
    required=True,
)
@click.option(
    "--modelId",
    "modelId",
    required=True,
)
@click.option(
    "--name",
    "name",
    required=True,
)
@click.option(
    "--tag",
    "tag",
)
@click.option(
    "--code",
    "code"
)
@click.option(
    "--cluster",
    "cluster",
)
@click.option(
    "--machineType",
    "machineType",
    required=True,
)
@click.option(
    "--imageUrl",
    "imageUrl",
    required=True,
)
@click.option(
    "--imageUsername",
    "imageUsername",
)
@click.option(
    "--imagePassword",
    "imagePassword",
)
@click.option(
    "--workspaceUrl",
    "workspaceUrl",
)
@click.option(
    "--workspaceUsername",
    "workspaceUsername",
)
@click.option(
    "--workspacePassword",
    "workspacePassword",
)
@click.option(
    "--instanceCount",
    "instanceCount",
    type=int,
    required=True,
)
@click.option(
    "--authToken",
    "authToken",
)
@click.option(
    "--oauthKey",
    "oauthKey",
)
@click.option(
    "--oauthSecret",
    "oauthSecret",
)
@click.option(
    "--serviceType",
    "serviceType",
)
@click.option(
    "--apiType",
    "apiType",
)
@click.option(
    "--ports",
    "ports",
)
def create_deployment(**kwargs):
    del_if_value_is_none(kwargs)
    command = deployments_commands.CreateDeployment()
    command.execute(kwargs)


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


@deployments.command("list")
@click.option(
    "--state",
    "state",
    type=ChoiceType(DEPLOYMENT_STATES_MAP, case_sensitive=False)
)
def get_deployments_list(**kwargs):
    command = deployments_commands.ListDeployments()
    command.execute(kwargs)


@deployments.command("update")
@click.option(
    "--id",
    "id",
    required=True,
)
@click.option(
    "--name",
    "name",
)
@click.option(
    "--tag",
    "tag",
)
@click.option(
    "--params",
    "params",
)
@click.option(
    "--code",
    "code",
)
@click.option(
    "--cluster",
    "cluster",
)
@click.option(
    "--machineType",
    "machineType",
)
@click.option(
    "--imageUrl",
    "imageUrl",
)
@click.option(
    "--imageUsername",
    "imageUsername",
)
@click.option(
    "--imagePassword",
    "imagePassword",
)
@click.option(
    "--workspaceUrl",
    "workspaceUrl",
)
@click.option(
    "--workspaceUsername",
    "workspaceUsername",
)
@click.option(
    "--workspacePassword",
    "workspacePassword",
)
@click.option(
    "--instanceCount",
    "instanceCount",
)
@click.option(
    "--authToken",
    "authToken",
)
@click.option(
    "--annotations",
    "annotations",
)
@click.option(
    "--authToken",
    "authToken",
)
@click.option(
    "--oauthKey",
    "oauthKey",
)
@click.option(
    "--oauthSecret",
    "oauthSecret",
)
@click.option(
    "--serviceType",
    "serviceType",
)
@click.option(
    "--apiType",
    "apiType",
)
@click.option(
    "--ports",
    "ports",
)
def update_deployment_model(id=None, **kwargs):
    del_if_value_is_none(kwargs)
    command = deployments_commands.UpdateModelCommand()
    command.execute(id, kwargs)


@deployments.command("start")
@click.option(
    "--id",
    "id",
    required=True,
)
def start_deployment(id):
    command = deployments_commands.StartDeployment()
    command.execute(id)


@deployments.command("delete")
@click.option(
    "--id",
    "id",
    required=True,
)
def delete_deployment(id):
    command = deployments_commands.DeleteDeployment()
    command.execute(id)
