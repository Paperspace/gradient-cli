import click

from gradient.api_sdk import constants
from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.cli_types import ChoiceType, json_string
from gradient.cli.common import validate_comma_split_option
from gradient.commands import models as models_commands


@cli.group("models", help="Manage models", cls=common.ClickGroup)
def models_group():
    pass


@models_group.group("tags", help="Manage model tags", cls=common.ClickGroup)
def model_tags():
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
@click.option(
    "--tag",
    "tags",
    multiple=True,
    cls=common.GradientOption,
    help="Filter by tags. Multiple use"
)
@common.api_key_option
@common.options_file
def list_models(api_key, experiment_id, project_id, tags, options_file):
    command = models_commands.ListModelsCommand(api_key=api_key)
    command.execute(experiment_id=experiment_id, project_id=project_id, tags=tags)


@models_group.command("delete", help="Delete model")
@click.option(
    "--id",
    "model_id",
    required=True,
    help="Model ID",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def delete_model(api_key, model_id, options_file):
    command = models_commands.DeleteModelCommand(api_key=api_key)
    command.execute(model_id=model_id)


@models_group.command("create", help="Create a model from an url or dataset id")
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
    "--datasetRef",
    "dataset_ref",
    required=True,
    help="Dataset ref to associate a model with",
    cls=common.GradientOption,
)
@click.option(
    "--projectId",
    "project_id",
    help="ID of a project",
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
@common.api_key_option
@common.options_file
def create_model(api_key, options_file, **model):
    model["tags"] = validate_comma_split_option(model.pop("tags_comma"), model.pop("tags"))
    command = models_commands.CreateModel(api_key=api_key)
    command.execute(**model)


@models_group.command("upload", help="Upload a model file or directory")
@click.argument(
    "PATH",
    required=True,
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
    "--projectId",
    "project_id",
    help="ID of a project",
    cls=common.GradientOption,
)
@click.option(
    "--clusterId",
    "cluster_id",
    help="ID of a cluster",
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
@common.api_key_option
@common.options_file
def upload_model(api_key, options_file, **model):
    model["tags"] = validate_comma_split_option(model.pop("tags_comma"), model.pop("tags"))
    command = models_commands.UploadModel(api_key=api_key)
    command.execute(**model)


@models_group.command("details", help="Show model details")
@click.option(
    "--id",
    "model_id",
    required=True,
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
    required=True,
    help="Model ID",
    cls=common.GradientOption,
)
@click.option(
    "--destinationDir",
    "destination_directory",
    required=True,
    help="Destination directory",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def download_model_files(model_id, destination_directory, api_key, options_file):
    command = models_commands.DownloadModelFiles(api_key=api_key)
    command.execute(model_id, destination_directory)


@model_tags.command("add", help="Add tags to ml model")
@click.option(
    "--id",
    "id",
    required=True,
    cls=common.GradientOption,
    help="ID of the model",
)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    help="One or many tags that you want to add to ml model",
    cls=common.GradientOption
)
@click.option(
    "--tags",
    "tags_comma",
    help="Separated by comma tags that you want add to ml model",
    cls=common.GradientOption
)
@common.api_key_option
@common.options_file
def ml_model_add_tag(id, options_file, api_key, **kwargs):
    kwargs["tags"] = validate_comma_split_option(kwargs.pop("tags_comma"), kwargs.pop("tags"), raise_if_no_values=True)

    command = models_commands.MLModelAddTagsCommand(api_key=api_key)
    command.execute(id, **kwargs)


@model_tags.command("remove", help="Remove tags from ml model")
@click.option(
    "--id",
    "id",
    required=True,
    cls=common.GradientOption,
    help="ID of the model",
)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    help="One or many tags that you want to remove from ml model",
    cls=common.GradientOption
)
@click.option(
    "--tags",
    "tags_comma",
    help="Separated by comma tags that you want to remove from ml model",
    cls=common.GradientOption
)
@common.api_key_option
@common.options_file
def ml_model_remove_tags(id, options_file, api_key, **kwargs):
    kwargs["tags"] = validate_comma_split_option(kwargs.pop("tags_comma"), kwargs.pop("tags"), raise_if_no_values=True)

    command = models_commands.MLModelRemoveTagsCommand(api_key=api_key)
    command.execute(id, **kwargs)
