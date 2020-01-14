import click

from gradient.api_sdk import constants
from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.cli_types import ChoiceType, json_string
from gradient.commands import models as models_commands


@cli.group("models", help="Manage models", cls=common.ClickGroup)
def models_group():
    pass


@models_group.command("list", help="List models with optional filtering")
@click.option(
    "--experimentId",
    "experiment_id",
    help="Use to filter by experiment ID",
    cls=common.GradientOption,
)
@click.option(
    "--projectId",
    "project_id",
    help="Use to filter by project ID",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def list_models(api_key, experiment_id, project_id, options_file):
    command = models_commands.ListModelsCommand(api_key=api_key)
    command.execute(experiment_id=experiment_id, project_id=project_id)


@models_group.command("delete", help="Delete model")
@click.option(
    "--id",
    "model_id",
    help="Model ID",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def list_models(api_key, model_id, options_file):
    command = models_commands.DeleteModelCommand(api_key=api_key)
    command.execute(model_id=model_id)


@models_group.command("upload", help="Upload a model file or directory")
@click.argument(
    "PATH",
    type=click.Path(exists=True),
    cls=common.GradientArgument,
)
@click.option(
    "--name",
    "name",
    required=True,
    help="Model name",
    cls=common.GradientOption,
)
@click.option(
    "--modelType",
    "model_type",
    required=True,
    type=ChoiceType(constants.MODEL_TYPES_MAP, case_sensitive=False),
    help="Model type",
    cls=common.GradientOption,
)
@click.option(
    "--modelSummary",
    "model_summary",
    type=json_string,
    help="Model summary",
    cls=common.GradientOption,
)
@click.option(
    "--notes",
    "notes",
    help="Additional notes",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def upload_model(path, name, model_type, model_summary, notes, api_key, options_file):
    command = models_commands.UploadModel(api_key=api_key)
    command.execute(path, name, model_type, model_summary, notes)


@models_group.command("details", help="Show model details")
@click.option(
    "--id",
    "model_id",
    help="Model ID",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def model_details(model_id, api_key, options_file):
    command = models_commands.GetModelCommand(api_key=api_key)
    command.execute(model_id)


@models_group.command("download", help="Download model files")
@click.option(
    "--id",
    "model_id",
    help="Model ID",
    cls=common.GradientOption,
)
@click.option(
    "--destinationDir",
    "destination_directory",
    help="Destination directory",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def download_model_files(model_id, destination_directory, api_key, options_file):
    command = models_commands.DownloadModelFiles(api_key=api_key)
    command.execute(model_id, destination_directory)
