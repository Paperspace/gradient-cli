import click

from gradient.cli import common
from gradient.cli.cli import cli
from gradient.commands import tensorboards as tensorboards_commands


@cli.group("tensorboards", help="Manage tensorboards", cls=common.ClickGroup)
def tensorboards_group():
    pass


@tensorboards_group.command("create", help="Create new tensorboard")
@click.option(
    "--experiment",
    "experiments",
    multiple=True,
    required=True,
    help="IDs of experiments",
    cls=common.GradientOption,
)
@click.option(
    "--image",
    "image",
    help="Image",
    cls=common.GradientOption,
)
@click.option(
    "--username",
    "username",
    help="Username",
    cls=common.GradientOption,
)
@click.option(
    "--password",
    "password",
    help="Password",
    cls=common.GradientOption,
)
@click.option(
    "--instanceType",
    "instance_type",
    help="Instance type",
    cls=common.GradientOption,
)
@click.option(
    "--instanceSize",
    "instance_size",
    help="Instance size",
    cls=common.GradientOption,
)
@click.option(
    "--instancesCount",
    "instances_count",
    type=int,
    help="Instances count",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def create_tensorboard(api_key, options_file, **kwargs):
    command = tensorboards_commands.CreateTensorboardCommand(api_key=api_key)
    command.execute(**kwargs)


@tensorboards_group.command("details", help="Show details of a tensorboard")
@click.option(
    "--id",
    "id",
    required=True,
    help="Tensorboard ID",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def tensorboard_details(id, api_key, options_file):
    command = tensorboards_commands.GetTensorboardCommand(api_key=api_key)
    command.execute(id)


@tensorboards_group.command("list", help="Show list of tensorboards")
@common.api_key_option
@common.options_file
def list_tensorboards(api_key, options_file):
    command = tensorboards_commands.ListTensorboardsCommand(api_key=api_key)
    command.execute()


@tensorboards_group.command("add-experiments", help="Update tensorboard experiments")
@click.option(
    "--id",
    "id",
    required=True,
    help="Tensorboard ID",
    cls=common.GradientOption,
)
@click.option(
    "--experiment",
    "experiments",
    multiple=True,
    required=True,
    help="IDs of experiments",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def add_experiments_to_tensorboard(api_key, options_file, **kwargs):
    command = tensorboards_commands.AddExperimentToTensorboard(api_key=api_key)
    command.execute(**kwargs)


@tensorboards_group.command("remove-experiments", help="Update tensorboard experiments")
@click.option(
    "--id",
    "id",
    required=True,
    help="Tensorboard ID",
    cls=common.GradientOption,
)
@click.option(
    "--experiment",
    "experiments",
    multiple=True,
    required=True,
    help="IDs of experiments",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def remove_experiments_to_tensorboard(api_key, options_file, **kwargs):
    command = tensorboards_commands.RemoveExperimentToTensorboard(api_key=api_key)
    command.execute(**kwargs)
