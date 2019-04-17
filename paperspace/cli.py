import collections
import functools
import json
import re

import click

from paperspace import constants, client, config
from paperspace.commands import experiments as experiments_commands, deployments as deployments_commands, \
    machines as machines_commands


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


class Number(click.ParamType):
    name = "number"

    def convert(self, value, param, ctx):
        try:
            number = int(value)
        except ValueError:
            try:
                number = float(value)
            except ValueError:
                self.fail('{} is not a valid number'.format(value), param, ctx)

        return number


def json_string(val):
    """Wraps json.loads so the cli help shows proper option's type name instead of 'LOADS'"""
    return json.loads(val)


def del_if_value_is_none(dict_):
    """Remove all elements with value == None"""
    for key, val in list(dict_.items()):
        if val is None:
            del dict_[key]


api_key_option = click.option(
    "--apiKey",
    "api_key",
    help="API key to use this time only",
)


def validate_mutually_exclusive(options_1, options_2, error_message):
    used_option_in_options_1 = any(option is not None for option in options_1)
    used_option_in_options_2 = any(option is not None for option in options_2)
    if used_option_in_options_1 and used_option_in_options_2:
        raise click.UsageError(error_message)


def validate_email(ctx, param, value):
    if value is not None \
            and not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        raise click.BadParameter("Bad email address format")

    return value


@click.group()
def cli():
    pass


@cli.group("experiments", help="Manage experiments")
def experiments():
    pass


@experiments.group("create", help="Create new experiment")
def create_experiment():
    pass


@experiments.group(name="createAndStart", help="Create and start new experiment")
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
            type=int,
            help="Port to use in new experiment",
        ),
        click.option(
            "--workspaceUrl",
            "workspaceUrl",
            required=True,
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
            type=int,
            help="Cluster ID",
        ),
        click.option(
            "--experimentEnv",
            "experimentEnv",
            type=json_string,
            help="Environment variables in a JSON",
        ),
        click.option(
            "--triggerEventId",
            "triggerEventId",
            type=int,
            help="Trigger event ID",
        ),
        click.option(
            "--projectId",
            "projectId",
            type=int,
            help="Project ID",
        ),
        click.option(
            "--projectHandle",
            "projectHandle",
            required=True,
            help="Project handle",
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
    experiments_commands.create_experiment(kwargs, api=experiments_api)


@create_experiment.command(name="singlenode", help="Create single node experiment")
@common_experiments_create_options
@common_experiments_create_single_node_options
def create_single_node(api_key, **kwargs):
    kwargs["experimentTypeId"] = constants.ExperimentType.SINGLE_NODE
    del_if_value_is_none(kwargs)
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    experiments_commands.create_experiment(kwargs, api=experiments_api)


@create_and_start_experiment.command(name="multinode", help="Create and start new multi node experiment")
@common_experiments_create_options
@common_experiment_create_multi_node_options
def create_and_start_multi_node(api_key, **kwargs):
    del_if_value_is_none(kwargs)
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    experiments_commands.create_and_start_experiment(kwargs, api=experiments_api)


@create_and_start_experiment.command(name="singlenode", help="Create and start new single node experiment")
@common_experiments_create_options
@common_experiments_create_single_node_options
def create_and_start_single_node(api_key, **kwargs):
    kwargs["experimentTypeId"] = constants.ExperimentType.SINGLE_NODE
    del_if_value_is_none(kwargs)
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    experiments_commands.create_and_start_experiment(kwargs, api=experiments_api)


@experiments.command("start", help="Start experiment")
@click.argument("experiment-handle")
@api_key_option
def start_experiment(experiment_handle, api_key):
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    experiments_commands.start_experiment(experiment_handle, api=experiments_api)


@experiments.command("stop", help="Stop experiment")
@click.argument("experiment-handle")
@api_key_option
def stop_experiment(experiment_handle, api_key):
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    experiments_commands.stop_experiment(experiment_handle, api=experiments_api)


@experiments.command("list", help="List experiments")
@click.option("--projectHandle", "-p", "project_handles", multiple=True)
@api_key_option
def list_experiments(project_handles, api_key):
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    command = experiments_commands.ListExperimentsCommand(api=experiments_api)
    command.execute(project_handles)


@experiments.command("details", help="Show detail of an experiment")
@click.argument("experiment-handle")
@api_key_option
def get_experiment_details(experiment_handle, api_key):
    experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
    experiments_commands.get_experiment_details(experiment_handle, api=experiments_api)


# TODO: delete experiment - not implemented in the api
# TODO: modify experiment - not implemented in the api
# TODO: create experiment template?? What is the difference between experiment and experiment template?


DEPLOYMENT_TYPES_MAP = collections.OrderedDict(
    (
        ("TFSERVING", "Tensorflow Serving on K8s"),
        ("GRADIENT", "Gradient Jobs"),
    )
)


@cli.group("deployments", help="Manage deployments")
def deployments():
    pass


@deployments.command("create", help="Create new deployment")
@click.option(
    "--deploymentType",
    "deploymentType",
    type=ChoiceType(DEPLOYMENT_TYPES_MAP, case_sensitive=False),
    required=True,
    help="Model deployment type",
)
@click.option(
    "--modelId",
    "modelId",
    required=True,
    help="ID of a trained model",
)
@click.option(
    "--name",
    "name",
    required=True,
    help="Human-friendly name for new model deployment",
)
@click.option(
    "--machineType",
    "machineType",
    type=click.Choice(constants.MACHINE_TYPES),
    required=True,
    help="Type of machine for new deployment",
)
@click.option(
    "--imageUrl",
    "imageUrl",
    required=True,
    help="Docker image for model serving",
)
@click.option(
    "--instanceCount",
    "instanceCount",
    type=int,
    required=True,
    help="Number of machine instances",
)
@api_key_option
def create_deployment(api_key=None, **kwargs):
    del_if_value_is_none(kwargs)
    deployments_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = deployments_commands.CreateDeploymentCommand(api=deployments_api)
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


@deployments.command("list", help="List deployments with optional filtering")
@click.option(
    "--state",
    "state",
    type=ChoiceType(DEPLOYMENT_STATES_MAP, case_sensitive=False),
    help="Filter by deployment state",
)
@api_key_option
def get_deployments_list(api_key=None, **kwargs):
    del_if_value_is_none(kwargs)
    deployments_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = deployments_commands.ListDeploymentsCommand(api=deployments_api)
    command.execute(kwargs)


@deployments.command("update", help="Update deployment properties")
@click.option(
    "--id",
    "id_",
    required=True,
    help="Deployment ID",
)
@click.option(
    "--modelId",
    "modelId",
    help="ID of a trained model",
)
@click.option(
    "--name",
    "name",
    help="Human-friendly name for new model deployment",
)
@click.option(
    "--machineType",
    "machineType",
    help="Type of machine for new deployment",
)
@click.option(
    "--imageUrl",
    "imageUrl",
    help="Docker image for model serving",
)
@click.option(
    "--instanceCount",
    "instanceCount",
    type=int,
    help="Number of machine instances",
)
@api_key_option
def update_deployment_model(id_, api_key, **kwargs):
    del_if_value_is_none(kwargs)
    deployments_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = deployments_commands.UpdateModelCommand(api=deployments_api)
    command.execute(id_, kwargs)


@deployments.command("start", help="Start deployment")
@click.option(
    "--id",
    "id_",
    required=True,
    help="Deployment ID",
)
@api_key_option
def start_deployment(id_, api_key=None):
    deployments_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = deployments_commands.StartDeploymentCommand(api=deployments_api)
    command.execute(id_)


@deployments.command("delete", help="Delete deployment")
@click.option(
    "--id",
    "id_",
    required=True,
    help="Deployment ID",
)
@api_key_option
def delete_deployment(id_, api_key=None):
    deployments_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = deployments_commands.DeleteDeploymentCommand(api=deployments_api)
    command.execute(id_)


REGIONS_MAP = collections.OrderedDict(
    (
        ("CA1", constants.Region.CA1),
        ("NY2", constants.Region.NY2),
        ("AMS1", constants.Region.AMS1),
    )
)


@cli.group("machines", help="Manage machines")
def machines_group():
    pass


check_machine_availability_help = "Get machine availability for the given region and machine type. " \
                                  "Note: availability is only provided for the dedicated GPU machine types. " \
                                  "Also, not all machine types are available in all regions"


@machines_group.command("availability", help=check_machine_availability_help)
@click.option(
    "--region",
    "region",
    type=ChoiceType(REGIONS_MAP, case_sensitive=False),
    required=True,
    help="Name of the region",
)
@click.option(
    "--machineType",
    "machine_type",
    type=click.Choice(constants.MACHINE_TYPES),
    required=True,
    help="Machine type",
)
@api_key_option
def check_machine_availability(region, machine_type, api_key):
    machines_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = machines_commands.CheckAvailabilityCommand(api=machines_api)
    command.execute(region, machine_type)


create_machine_help = "Create a new Paperspace virtual machine. If you are using an individual account, you will " \
                      "be assigned as the owner of the machine. If you are a team administrator, you must specify " \
                      "the user that should be assigned to the machine, either by specifing a user id, or by " \
                      "providing an email address, password, first name and last name for the creation of a new " \
                      "user on the team."


@machines_group.command("create", help=create_machine_help)
@click.option(
    "--region",
    "region",
    type=ChoiceType(REGIONS_MAP, case_sensitive=False),
    required=True,
    help="Name of the region",
)
@click.option(
    "--machineType",
    "machineType",
    type=click.Choice(constants.MACHINE_TYPES),
    required=True,
    help="Machine type",
)
@click.option(
    "--size",
    "size",
    type=int,
    required=True,
    help="Storage size for the machine in GB",
)
@click.option(
    "--billingType",
    "billingType",
    type=click.Choice(constants.BILLING_TYPES),
    required=True,
    help="Either 'monthly' or 'hourly' billing",
)
@click.option(
    "--machineName",
    "machineName",
    required=True,
    help="A memorable name for this machine",
)
@click.option(
    "--templateId",
    "templateId",
    required=True,
    help="Template id of the template to use for creating this machine",
)
@click.option(
    "--assignPublicIp",
    "assignPublicIp",
    is_flag=True,
    default=None,  # None is used so it can be filtered with `del_if_value_is_none` when flag was not set
    help="Assign a new public ip address on machine creation. Cannot be used with dynamicPublicIp",
)
@click.option(
    "--dynamicPublicIp",
    "dynamicPublicIp",
    is_flag=True,
    default=None,  # None is used so it can be filtered with `del_if_value_is_none` when flag was not set
    help="Assigns a new public ip address on machine start and releases it from the account on machine stop. "
         "Cannot be used with assignPublicIp",
)
@click.option(
    "--networkId",
    "networkId",
    help="If creating on a specific network, specify its id",
)
@click.option(
    "--teamId",
    "teamId",
    help="If creating the machine for a team, specify the team id",
)
@click.option(
    "--userId",
    "userId",
    help="If assigning to an existing user other than yourself, specify the user id (mutually exclusive with email, "
         "password, firstName, lastName)"
)
@click.option(
    "--email",
    "email",
    help="If creating a new user for this machine, specify their email address (mutually exclusive with userId)",
    callback=validate_email,
)
@click.option(
    "--password",
    "password",
    help="If creating a new user, specify their password (mutually exclusive with userId)",
)
@click.option(
    "--firstName",
    "firstName",
    help="If creating a new user, specify their first name (mutually exclusive with userId)",
)
@click.option(
    "--lastName",
    "lastName",
    help="If creating a new user, specify their last name (mutually exclusive with userId)",
)
@click.option(
    "--notificationEmail",
    "notificationEmail",
    help="Send a notification to this email address when complete",
    callback=validate_email,
)
@click.option(
    "--scriptId",
    "scriptId",
    help="The script id of a script to be run on startup. See the Script Guide for more info on using scripts",
)
@api_key_option
def create_machine(api_key, **kwargs):
    del_if_value_is_none(kwargs)

    assign_public_ip = kwargs.get("assignPublicIp")
    dynamic_public_ip = kwargs.get("dynamicPublicIp")
    validate_mutually_exclusive([assign_public_ip], [dynamic_public_ip],
                                "--assignPublicIp cannot be used with --dynamicPublicIp")

    team_id = kwargs.get("teamId")
    email = kwargs.get("email")
    password = kwargs.get("password")
    first_name = kwargs.get("firstName")
    last_name = kwargs.get("lastName")
    validate_mutually_exclusive([team_id], [email, password, first_name, last_name],
                                "--userId is mutually exclusive with --email, --password, --firstName and --lastName")

    machines_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = machines_commands.CreateMachineCommand(api=machines_api)
    command.execute(kwargs)


destroy_machine_help = "Destroy the machine with the given id. When this action is performed, the machine is " \
                       "immediately shut down and marked for deletion from the datacenter. Any snapshots that " \
                       "were derived from the machine are also deleted. Access to the machine is terminated " \
                       "immediately and billing for the machine is prorated to the hour. This action can only " \
                       "be performed by the user who owns the machine, or in the case of a team, the team " \
                       "administrator."


@machines_group.command("destroy", help=destroy_machine_help)
@click.option(
    "--machineId",
    "machine_id",
    required=True,
    help="The id of the machine to destroy",
)
@click.option(
    "--releasePublicIp",
    "release_public_ip",
    is_flag=True,
    help="releases any assigned public ip address for the machine; defaults to false",
)
@api_key_option
def destroy_machine(machine_id, release_public_ip, api_key):
    machines_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = machines_commands.DestroyMachineCommand(api=machines_api)
    command.execute(machine_id, release_public_ip)


list_machines_help = "List information about all machines available to either the current authenticated user or " \
                     "the team, if the user belongs to a team. The list method takes an optional first argument " \
                     "to limit the returned machine objects."


@machines_group.command("list", help=list_machines_help)
@click.option(
    "--params",
    "params",
    type=json_string,
    help="JSON used to filter machines. Use either this or a combination of following options"
)
@click.option(
    "--machineId",
    "machineId",
    help="Optional machine id to match on",
)
@click.option(
    "--name",
    "name",
    help="Filter by machine name",
)
@click.option(
    "--os",
    "os",
    help="Filter by os used",
)
@click.option(
    "--ram",
    "ram",
    type=int,
    help="Filter by machine RAM (in bytes)",
)
@click.option(
    "--cpus",
    "cpus",
    type=int,
    help="Filter by CPU count",
)
@click.option(
    "--gpu",
    "gpu",
    help="Filter by GPU type",
)
@click.option(
    "--storageTotal",
    "storageTotal",
    help="Filter by total storage",
)
@click.option(
    "--storageUsed",
    "storageUsed",
    help="Filter by storage used",
)
@click.option(
    "--usageRate",
    "usageRate",
    help="Filter by usage rate",
)
@click.option(
    "--shutdownTimeoutInHours",
    "shutdownTimeoutInHours",
    type=int,
    help="Filter by shutdown timeout",
)
@click.option(
    "--performAutoSnapshot",
    "performAutoSnapshot",
    type=bool,
    help="Filter by performAutoSnapshot flag",
)
@click.option(
    "--autoSnapshotFrequency",
    "autoSnapshotFrequency",
    type=click.Choice(["hour", "day", "week"], case_sensitive=False),
    help="Filter by autoSnapshotFrequency flag",
)
@click.option(
    "--autoSnapshotSaveCount",
    "autoSnapshotSaveCount",
    type=int,
    help="Filter by auto shapshots count",
)
@click.option(
    "--agentType",
    "agentType",
    help="Filter by agent type",
)
@click.option(
    "--dtCreated",
    "dtCreated",
    help="Filter by date created",
)
@click.option(
    "--state",
    "state",
    help="Filter by state",
)
@click.option(
    "--updatesPending",
    "updatesPending",
    help="Filter by updatesPending",
)
@click.option(
    "--networkId",
    "networkId",
    help="Filter by network ID",
)
@click.option(
    "--privateIpAddress",
    "privateIpAddress",
    help="Filter by private IP address",
)
@click.option(
    "--publicIpAddress",
    "publicIpAddress",
    help="Filter by public IP address",
)
@click.option(
    "--region",
    "region",
    type=ChoiceType(REGIONS_MAP, case_sensitive=False),
    help="Filter by region",
)
@click.option(
    "--userId",
    "userId",
    help="Filter by user ID",
)
@click.option(
    "--teamId",
    "teamId",
    help="Filter by team ID",
)
@click.option(
    "--dtLastRun",
    "dtLastRun",
    help="Filter by last run date",
)
@api_key_option
def list_machines(api_key, params, **kwargs):
    del_if_value_is_none(kwargs)
    params = params or {}
    kwargs = kwargs or {}
    validate_mutually_exclusive(params.values(), kwargs.values(),
                                "You can use either --params dictionary or single filter arguments")

    machines_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = machines_commands.ListMachinesCommand(api=machines_api)
    command.execute(params or kwargs)


restart_machine_help = "Restart an individual machine. If the machine is already restarting, this action will " \
                       "request the machine be restarted again. This action can only be performed by the user " \
                       "who owns the machine"


@machines_group.command("restart", help=restart_machine_help)
@click.option(
    "--machineId",
    "machine_id",
    help="Id of the machine to restart",
    required=True,
)
@api_key_option
def restart_machine(machine_id, api_key):
    machines_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = machines_commands.RestartMachineCommand(api=machines_api)
    command.execute(machine_id)


show_machine_details_help = "Show machine information for the machine with the given id."


@machines_group.command("show", help=show_machine_details_help)
@click.option(
    "--machineId",
    "machine_id",
    help="Id of the machine to show",
    required=True,
)
@api_key_option
def show_machine_details(machine_id, api_key):
    machines_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = machines_commands.ShowMachineCommand(api=machines_api)
    command.execute(machine_id)


update_machine_help = "Update attributes of a machine"


@machines_group.command("update", help=update_machine_help)
@click.option(
    "--machineId",
    "machine_id",
    help="Id of the machine to update",
    required=True,
)
@click.option(
    "--machineName",
    "machineName",
    help="New name for the machine",
)
@click.option(
    "--shutdownTimeoutInHours",
    "shutdownTimeoutInHours",
    help="Number of hours before machine is shutdown if no one is logged in via the Paperspace client",
    type=int,
)
@click.option(
    "--shutdownTimeoutForces",
    "shutdownTimeoutForces",
    help="Force shutdown at shutdown timeout, even if there is a Paperspace client connection",
    type=bool,
)
@click.option(
    "--performAutoSnapshot",
    "performAutoSnapshot",
    help="Perform auto snapshots",
    type=bool,
)
@click.option(
    "--autoSnapshotFrequency",
    "autoSnapshotFrequency",
    help="One of 'hour', 'day', 'week', or null",
    type=click.Choice(["hour", "day", "week"], case_sensitive=False),
)
@click.option(
    "--autoSnapshotSaveCount",
    "autoSnapshotSaveCount",
    help="Number of snapshots to save",
    type=int,
)
@click.option(
    "--dynamicPublicIp",
    "dynamicPublicIp",
    help="If true, assigns a new public ip address on machine start and releases it from the account on machine stop",
    type=bool,
)
@api_key_option
def update_machine(machine_id, api_key, **kwargs):
    del_if_value_is_none(kwargs)
    machines_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = machines_commands.UpdateMachineCommand(api=machines_api)
    command.execute(machine_id, kwargs)


start_machine_help = "Start up an individual machine. If the machine is already started, this action is a no-op. " \
                     "If the machine is off, it will be booted up. This action can only be performed by the user " \
                     "who owns the machine"


@machines_group.command("start", help=start_machine_help)
@click.option(
    "--machineId",
    "machine_id",
    help="Id of the machine to start",
    required=True,
)
@api_key_option
def start_machine(machine_id, api_key):
    machines_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = machines_commands.StartMachineCommand(api=machines_api)
    command.execute(machine_id)


stop_machine_help = "Stop an individual machine. If the machine is already stopped or has been shut down, this " \
                    "action is a no-op. If the machine is running, it will be stopped and any users logged in " \
                    "will be immediately kicked out. This action can only be performed by the user who owns the machine"


@machines_group.command("stop", help=stop_machine_help)
@click.option(
    "--machineId",
    "machine_id",
    help="Id of the machine to start",
    required=True,
)
@api_key_option
def stop_machine(machine_id, api_key):
    machines_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = machines_commands.StopMachineCommand(api=machines_api)
    command.execute(machine_id)


show_machine_utilization_help = "Get machine utilization data for the machine with the given id. Machine upgrades " \
                                "are not represented in utilization data"


@machines_group.command("utilization", help=show_machine_utilization_help)
@click.option(
    "--machineId",
    "machine_id",
    help="Id of the machine to start",
    required=True,
)
@click.option(
    "--billingMonth",
    "billing_month",
    required=True,
    help="Month in YYYY-MM format",
)
@api_key_option
def show_machine_utilization(machine_id, billing_month, api_key):
    machines_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = machines_commands.ShowMachineUtilisationCommand(api=machines_api)
    command.execute(machine_id, billing_month)


wait_for_machine_state_help = "Wait for the machine with the given id to enter a certain machine state. " \
                              "This action polls the server and returns only when we detect that the machine " \
                              "has transitioned into the given state."


@machines_group.command("waitfor", help=wait_for_machine_state_help)
@click.option(
    "--machineId",
    "machine_id",
    help="Id of the machine to start",
    required=True,
)
@click.option(
    "--state",
    "state",
    help="Name of the state to wait for",
    type=click.Choice(["off", "serviceready", "ready"], case_sensitive=False),
    required=True,
)
@api_key_option
def wait_for_machine_state(machine_id, state, api_key):
    machines_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = machines_commands.WaitForMachineStateCommand(api=machines_api)
    command.execute(machine_id, state)
