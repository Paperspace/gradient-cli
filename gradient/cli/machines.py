import collections

import click

from gradient import clilogger
from gradient.api_sdk import constants
from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.cli_types import ChoiceType, json_string
from gradient.cli.common import api_key_option, del_if_value_is_none, ClickGroup, validate_comma_split_option
from gradient.cli.validators import validate_email, validate_mutually_exclusive
from gradient.commands import machines as machines_commands

REGIONS_MAP = collections.OrderedDict(
    (
        ("CA1", constants.Region.CA1),
        ("NY2", constants.Region.NY2),
        ("AMS1", constants.Region.AMS1),
    )
)


@cli.group("machines", help="Manage machines", cls=ClickGroup)
def machines_group():
    pass


@machines_group.group("tags", help="Manage machine tags", cls=ClickGroup)
def machines_tags():
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
    cls=common.GradientOption,
)
@click.option(
    "--machineType",
    "machine_type",
    required=True,
    help="Machine type",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def check_machine_availability(region, machine_type, api_key, options_file):
    command = machines_commands.CheckAvailabilityCommand(api_key=api_key)
    command.execute(machine_type, region)


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
    cls=common.GradientOption,
)
@click.option(
    "--machineType",
    "machine_type",
    required=True,
    help="Machine type",
    cls=common.GradientOption,
)
@click.option(
    "--size",
    "size",
    type=int,
    required=True,
    help="Storage size for the machine in GB",
    cls=common.GradientOption,
)
@click.option(
    "--billingType",
    "billing_type",
    type=click.Choice(constants.BILLING_TYPES),
    required=True,
    help="Either 'monthly' or 'hourly' billing",
    cls=common.GradientOption,
)
@click.option(
    "--machineName",
    "name",
    required=True,
    help="A memorable name for this machine",
    cls=common.GradientOption,
)
@click.option(
    "--templateId",
    "template_id",
    required=True,
    help="Template id of the template to use for creating this machine",
    cls=common.GradientOption,
)
@click.option(
    "--assignPublicIp",
    "assign_public_ip",
    is_flag=True,
    default=None,  # None is used so it can be filtered with `del_if_value_is_none` when flag was not set
    help="Assign a new public ip address on machine creation. Cannot be used with dynamicPublicIp",
    cls=common.GradientOption,
)
@click.option(
    "--dynamicPublicIp",
    "dynamic_public_ip",
    is_flag=True,
    default=None,  # None is used so it can be filtered with `del_if_value_is_none` when flag was not set
    help="Assigns a new public ip address on machine start and releases it from the account on machine stop. "
         "Cannot be used with assignPublicIp",
    cls=common.GradientOption,
)
@click.option(
    "--networkId",
    "network_id",
    help="If creating on a specific network, specify its id",
    cls=common.GradientOption,
)
@click.option(
    "--teamId",
    "team_id",
    help="If creating the machine for a team, specify the team id",
    cls=common.GradientOption,
)
@click.option(
    "--userId",
    "user_id",
    help="If assigning to an existing user other than yourself, specify the user id (mutually exclusive with email, "
         "password, firstName, lastName)",
    cls=common.GradientOption,
)
@click.option(
    "--email",
    "email",
    help="If creating a new user for this machine, specify their email address (mutually exclusive with userId)",
    callback=validate_email,
    cls=common.GradientOption,
)
@click.option(
    "--password",
    "password",
    help="If creating a new user, specify their password (mutually exclusive with userId)",
    cls=common.GradientOption,
)
@click.option(
    "--firstName",
    "first_name",
    help="If creating a new user, specify their first name (mutually exclusive with userId)",
    cls=common.GradientOption,
)
@click.option(
    "--lastName",
    "last_name",
    help="If creating a new user, specify their last name (mutually exclusive with userId)",
    cls=common.GradientOption,
)
@click.option(
    "--notificationEmail",
    "notification_email",
    help="Send a notification to this email address when complete",
    callback=validate_email,
    cls=common.GradientOption,
)
@click.option(
    "--scriptId",
    "script_id",
    help="The script id of a script to be run on startup. See the Script Guide for more info on using scripts",
    cls=common.GradientOption,
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
def create_machine(api_key, options_file, **kwargs):
    kwargs["tags"] = validate_comma_split_option(kwargs.pop("tags_comma"), kwargs.pop("tags"))
    del_if_value_is_none(kwargs)

    assign_public_ip = kwargs.get("assign_public_ip")
    dynamic_public_ip = kwargs.get("dynamic_public_ip")
    validate_mutually_exclusive([assign_public_ip], [dynamic_public_ip],
                                "--assignPublicIp cannot be used with --dynamicPublicIp")

    user_id = kwargs.get("user_id")
    email = kwargs.get("email")
    password = kwargs.get("password")
    first_name = kwargs.get("first_name")
    last_name = kwargs.get("last_name")
    validate_mutually_exclusive([user_id], [email, password, first_name, last_name],
                                "--userId is mutually exclusive with --email, --password, --firstName and --lastName")

    command = machines_commands.CreateMachineCommand(api_key=api_key, logger=clilogger.CliLogger())
    command.execute(kwargs)


destroy_machine_help = "Destroy the machine with the given id. When this action is performed, the machine is " \
                       "immediately shut down and marked for deletion from the datacenter. Any snapshots that " \
                       "were derived from the machine are also deleted. Access to the machine is terminated " \
                       "immediately and billing for the machine is prorated to the hour. This action can only " \
                       "be performed by the user who owns the machine, or in the case of a team, the team " \
                       "administrator."


@machines_group.command("destroy", help=destroy_machine_help)
@click.option(
    "--id",
    "machine_id",
    required=True,
    help="The id of the machine to destroy",
    cls=common.GradientOption,
)
@click.option(
    "--releasePublicIp",
    "release_public_ip",
    is_flag=True,
    help="releases any assigned public ip address for the machine; defaults to false",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def destroy_machine(machine_id, release_public_ip, api_key, options_file):
    command = machines_commands.DestroyMachineCommand(api_key=api_key, logger=clilogger.CliLogger())
    command.execute(machine_id, release_public_ip)


list_machines_help = "List information about all machines available to either the current authenticated user or " \
                     "the team, if the user belongs to a team. The list method takes an optional first argument " \
                     "to limit the returned machine objects."


@machines_group.command("list", help=list_machines_help)
@click.option(
    "--params",
    "params",
    type=json_string,
    help="JSON used to filter machines. Use either this or a combination of following options",
    cls=common.GradientOption,
)
@click.option(
    "--id",
    "id",
    help="Optional machine id to match on",
    cls=common.GradientOption,
)
@click.option(
    "--name",
    "name",
    help="Filter by machine name",
    cls=common.GradientOption,
)
@click.option(
    "--os",
    "os",
    help="Filter by os used",
    cls=common.GradientOption,
)
@click.option(
    "--ram",
    "ram",
    type=int,
    help="Filter by machine RAM (in bytes)",
    cls=common.GradientOption,
)
@click.option(
    "--cpus",
    "cpus",
    type=int,
    help="Filter by CPU count",
    cls=common.GradientOption,
)
@click.option(
    "--gpu",
    "gpu",
    help="Filter by GPU type",
    cls=common.GradientOption,
)
@click.option(
    "--storageTotal",
    "storage_total",
    help="Filter by total storage",
    cls=common.GradientOption,
)
@click.option(
    "--storageUsed",
    "storage_used",
    help="Filter by storage used",
    cls=common.GradientOption,
)
@click.option(
    "--usageRate",
    "usage_rate",
    help="Filter by usage rate",
    cls=common.GradientOption,
)
@click.option(
    "--shutdownTimeoutInHours",
    "shutdown_timeout_in_hours",
    type=int,
    help="Filter by shutdown timeout",
    cls=common.GradientOption,
)
@click.option(
    "--performAutoSnapshot",
    "perform_auto_snapshot",
    type=bool,
    help="Filter by performAutoSnapshot flag",
    cls=common.GradientOption,
)
@click.option(
    "--autoSnapshotFrequency",
    "auto_snapshot_frequency",
    type=click.Choice(["hour", "day", "week"], case_sensitive=False),
    help="Filter by autoSnapshotFrequency flag",
    cls=common.GradientOption,
)
@click.option(
    "--autoSnapshotSaveCount",
    "auto_snapshot_save_count",
    type=int,
    help="Filter by auto shapshots count",
    cls=common.GradientOption,
)
@click.option(
    "--agentType",
    "agent_type",
    help="Filter by agent type",
    cls=common.GradientOption,
)
@click.option(
    "--dtCreated",
    "created_timestamp",
    help="Filter by date created",
    cls=common.GradientOption,
)
@click.option(
    "--state",
    "state",
    help="Filter by state",
    cls=common.GradientOption,
)
@click.option(
    "--updatesPending",
    "updates_pending",
    help="Filter by updatesPending",
    cls=common.GradientOption,
)
@click.option(
    "--networkId",
    "network_id",
    help="Filter by network ID",
    cls=common.GradientOption,
)
@click.option(
    "--privateIpAddress",
    "private_ip_address",
    help="Filter by private IP address",
    cls=common.GradientOption,
)
@click.option(
    "--publicIpAddress",
    "public_ip_address",
    help="Filter by public IP address",
    cls=common.GradientOption,
)
@click.option(
    "--region",
    "region",
    type=ChoiceType(REGIONS_MAP, case_sensitive=False),
    help="Filter by region",
    cls=common.GradientOption,
)
@click.option(
    "--userId",
    "user_id",
    help="Filter by user ID",
    cls=common.GradientOption,
)
@click.option(
    "--teamId",
    "team_id",
    help="Filter by team ID",
    cls=common.GradientOption,
)
@click.option(
    "--dtLastRun",
    "last_run_timestamp",
    help="Filter by last run date",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def list_machines(api_key, params, options_file, **kwargs):
    del_if_value_is_none(kwargs)
    params = params or {}
    kwargs = kwargs or {}
    validate_mutually_exclusive(params.values(), kwargs.values(),
                                "You can use either --params dictionary or single filter arguments")

    command = machines_commands.ListMachinesCommand(api_key=api_key, logger=clilogger.CliLogger())
    filters = params or kwargs
    command.execute(**filters)


restart_machine_help = "Restart an individual machine. If the machine is already restarting, this action will " \
                       "request the machine be restarted again. This action can only be performed by the user " \
                       "who owns the machine"


@machines_group.command("restart", help=restart_machine_help)
@click.option(
    "--id",
    "machine_id",
    help="Id of the machine to restart",
    required=True,
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def restart_machine(machine_id, api_key, options_file):
    command = machines_commands.RestartMachineCommand(api_key=api_key, logger=clilogger.CliLogger())
    command.execute(machine_id)


show_machine_details_help = "Show machine information for the machine with the given id."


@machines_group.command("details", help=show_machine_details_help)
@click.option(
    "--id",
    "machine_id",
    help="Id of the machine to show",
    required=True,
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def show_machine_details(machine_id, api_key, options_file):
    command = machines_commands.ShowMachineCommand(api_key=api_key)
    command.execute(machine_id)


update_machine_help = "Update attributes of a machine"


@machines_group.command("update", help=update_machine_help)
@click.option(
    "--id",
    "machine_id",
    help="Id of the machine to update",
    required=True,
    cls=common.GradientOption,
)
@click.option(
    "--machineName",
    "name",
    help="New name for the machine",
    cls=common.GradientOption,
)
@click.option(
    "--shutdownTimeoutInHours",
    "shutdown_timeout_in_hours",
    help="Number of hours before machine is shutdown if no one is logged in via the Paperspace client",
    type=int,
    cls=common.GradientOption,
)
@click.option(
    "--shutdownTimeoutForces",
    "shutdown_timeout_forces",
    help="Force shutdown at shutdown timeout, even if there is a Paperspace client connection",
    type=bool,
    cls=common.GradientOption,
)
@click.option(
    "--performAutoSnapshot",
    "perform_auto_snapshot",
    help="Perform auto snapshots",
    type=bool,
    cls=common.GradientOption,
)
@click.option(
    "--autoSnapshotFrequency",
    "auto_snapshot_frequency",
    help="One of 'hour', 'day', 'week', or null",
    type=click.Choice(["hour", "day", "week"], case_sensitive=False),
    cls=common.GradientOption,
)
@click.option(
    "--autoSnapshotSaveCount",
    "auto_snapshot_save_count",
    help="Number of snapshots to save",
    type=int,
    cls=common.GradientOption,
)
@click.option(
    "--dynamicPublicIp",
    "dynamic_public_ip",
    help="If true, assigns a new public ip address on machine start and releases it from the account on machine stop",
    type=bool,
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def update_machine(machine_id, api_key, options_file, **kwargs):
    del_if_value_is_none(kwargs)
    command = machines_commands.UpdateMachineCommand(api_key=api_key)
    command.execute(machine_id, kwargs)


start_machine_help = "Start up an individual machine. If the machine is already started, this action is a no-op. " \
                     "If the machine is off, it will be booted up. This action can only be performed by the user " \
                     "who owns the machine"


@machines_group.command("start", help=start_machine_help)
@click.option(
    "--id",
    "machine_id",
    help="Id of the machine to start",
    required=True,
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def start_machine(machine_id, api_key, options_file):
    command = machines_commands.StartMachineCommand(api_key=api_key)
    command.execute(machine_id)


stop_machine_help = "Stop an individual machine. If the machine is already stopped or has been shut down, this " \
                    "action is a no-op. If the machine is running, it will be stopped and any users logged in " \
                    "will be immediately kicked out. This action can only be performed by the user who owns the machine"


@machines_group.command("stop", help=stop_machine_help)
@click.option(
    "--id",
    "machine_id",
    help="Id of the machine to start",
    required=True,
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def stop_machine(machine_id, api_key, options_file):
    command = machines_commands.StopMachineCommand(api_key=api_key)
    command.execute(machine_id)


show_machine_utilization_help = "Get machine utilization data for the machine with the given id. Machine upgrades " \
                                "are not represented in utilization data"


@machines_group.command("utilization", help=show_machine_utilization_help)
@click.option(
    "--id",
    "machine_id",
    help="Id of the machine to start",
    required=True,
    cls=common.GradientOption,
)
@click.option(
    "--billingMonth",
    "billing_month",
    required=True,
    help="Month in YYYY-MM format",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def show_machine_utilization(machine_id, billing_month, api_key, options_file):
    command = machines_commands.ShowMachineUtilizationCommand(api_key=api_key)
    command.execute(machine_id, billing_month)


wait_for_machine_state_help = "Wait for the machine with the given id to enter a certain machine state. " \
                              "This action polls the server and returns only when we detect that the machine " \
                              "has transitioned into the given state."


@machines_group.command("waitfor", help=wait_for_machine_state_help)
@click.option(
    "--id",
    "machine_id",
    help="Id of the machine to start",
    required=True,
    cls=common.GradientOption,
)
@click.option(
    "--state",
    "state",
    help="Name of the state to wait for",
    type=click.Choice(["off", "serviceready", "ready"], case_sensitive=False),
    required=True,
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def wait_for_machine_state(machine_id, state, api_key, options_file):
    command = machines_commands.WaitForMachineStateCommand(api_key=api_key)
    command.execute(machine_id, state)


@machines_tags.command("add", help="Add tags to machine")
@click.option(
    "--id",
    "id",
    required=True,
    cls=common.GradientOption,
    help="ID of the machine",
)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    help="One or many tags that you want to add to machine",
    cls=common.GradientOption
)
@click.option(
    "--tags",
    "tags_comma",
    help="Separated by comma tags that you want add to machine",
    cls=common.GradientOption
)
@api_key_option
@common.options_file
def machine_add_tag(id, options_file, api_key, **kwargs):
    kwargs["tags"] = validate_comma_split_option(kwargs.pop("tags_comma"), kwargs.pop("tags"), raise_if_no_values=True)

    command = machines_commands.MachineAddTagsCommand(api_key=api_key)
    command.execute(id, **kwargs)


@machines_tags.command("remove", help="Remove tags from machine")
@click.option(
    "--id",
    "id",
    required=True,
    cls=common.GradientOption,
    help="ID of the machine",
)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    help="One or many tags that you want to remove from machine",
    cls=common.GradientOption
)
@click.option(
    "--tags",
    "tags_comma",
    help="Separated by comma tags that you want to remove from machine",
    cls=common.GradientOption
)
@api_key_option
@common.options_file
def machine_remove_tags(id, options_file, api_key, **kwargs):
    kwargs["tags"] = validate_comma_split_option(kwargs.pop("tags_comma"), kwargs.pop("tags"), raise_if_no_values=True)

    command = machines_commands.MachineRemoveTagsCommand(api_key=api_key)
    command.execute(id, **kwargs)
