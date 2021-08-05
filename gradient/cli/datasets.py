import click

from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.common import ClickGroup, api_key_option
from gradient.commands import datasets as commands
from gradient.cli import common
from gradient.cli.common import api_key_option, ClickGroup

EXAMPLE_ID = 'dsr8k5qzn401lb5'
EXAMPLE_VERSION = 'klfoyy9'
EXAMPLE_TAG = 'prod'


def execute_list(command, **kwargs):
    for has_more in command.execute(**kwargs):
        if has_more:
            click.echo("")
            click.confirm("Do you want to continue?", abort=True)
            click.echo("")


def validate_dataset_id(dataset_ref, ref_type=None):
    dataset_part = EXAMPLE_ID
    full_part = dataset_part

    if ref_type == 'version':
        full_part += ':{}'.format(EXAMPLE_VERSION)
    elif ref_type == 'tag':
        full_part += ':{}'.format(EXAMPLE_TAG)
    elif ref_type:
        raise Exception('unknown ref type')

    dataset_id, _, ref = dataset_ref.partition(":")
    if not dataset_id:
        raise click.UsageError(
            "The '--id' option is missing the dataset ID (ex: {}})".format(full_part))
    if ref_type and not ref:
        raise click.UsageError(
            "The '--id' option is missing the {} (ex: {})".format(ref_type, full_part))
    elif not ref_type and ref:
        raise click.UsageError(
            "The '--id' option should not have a version/tag (ex: {})".format(full_part))


@cli.group("datasets", help="Manage datasets", cls=ClickGroup)
def datasets():
    pass


@datasets.command("list", help="List datasets")
@api_key_option
@common.options_file
def list_datasets(api_key, options_file):
    command = commands.ListDatasetsCommand(api_key=api_key)
    execute_list(command)


@datasets.command("details", help="Show dataset details")
@click.option(
    "--id",
    "dataset_id",
    help="Dataset ID",
    cls=common.GradientOption,
    required=True,
)
@common.api_key_option
@common.options_file
def show_dataset_details(dataset_id, api_key, options_file):
    validate_dataset_id(dataset_id)
    command = commands.ShowDatasetDetailsCommand(api_key=api_key)
    command.execute(dataset_id)


@datasets.command("create", help="Create dataset")
@click.option(
    "--name",
    "name",
    help="Dataset name",
    cls=common.GradientOption,
    required=True,
)
@click.option(
    "--storageProviderId",
    "storage_provider_id",
    help="Storage provider ID",
    cls=common.GradientOption,
    required=True,
)
@click.option(
    "--description",
    "description",
    help="Dataset description",
    cls=common.GradientOption,
    required=False,
)
@common.api_key_option
@common.options_file
def create_dataset(
        name,
        storage_provider_id,
        description,
        api_key,
        options_file,
):
    command = commands.CreateDatasetCommand(api_key=api_key)
    command.execute(
        name=name,
        description=description,
        storage_provider_id=storage_provider_id,
    )


@datasets.command("update", help="Update dataset")
@click.option(
    "--id",
    "dataset_id",
    help="Dataset ID",
    cls=common.GradientOption,
    required=True,
)
@click.option(
    "--name",
    "name",
    help="Dataset name",
    cls=common.GradientOption,
)
@click.option(
    "--description",
    "description",
    help="Dataset description",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def update_dataset(
        dataset_id,
        name,
        description,
        api_key,
        options_file,
):
    validate_dataset_id(dataset_id)
    command = commands.UpdateDatasetCommand(api_key=api_key)
    command.execute(
        dataset_id=dataset_id,
        name=name,
        description=description,
    )


@datasets.command("delete", help="Delete dataset")
@click.option(
    "--id",
    "dataset_id",
    help="Dataset ID",
    cls=common.GradientOption,
    required=True,
)
@common.api_key_option
@common.options_file
def delete_dataset(dataset_id, api_key, options_file):
    validate_dataset_id(dataset_id)
    command = commands.DeleteDatasetCommand(api_key=api_key)
    command.execute(dataset_id)


@datasets.group("tags", help="Manage tags", cls=ClickGroup)
def dataset_tags():
    pass


@dataset_tags.command("list", help="List dataset tags")
@click.option(
    "--id",
    "dataset_id",
    help="Dataset ID (ex: {})".format(EXAMPLE_ID),
    cls=common.GradientOption,
    required=True,
)
@api_key_option
@common.options_file
def list_dataset_tags(api_key, dataset_id, options_file):
    validate_dataset_id(dataset_id)
    command = commands.ListDatasetTagsCommand(api_key=api_key)
    execute_list(command, dataset_id=dataset_id)


@dataset_tags.command("set", help="Set dataset tag")
@click.option(
    "--id",
    "dataset_version_id",
    help="Dataset version ID (ex: {}:{})".format(EXAMPLE_ID, EXAMPLE_VERSION),
    cls=common.GradientOption,
    required=True,
)
@click.option(
    "--name",
    "name",
    help="Dataset tag name",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def set_dataset_tag(
        dataset_version_id,
        name,
        api_key,
        options_file,
):
    validate_dataset_id(dataset_version_id, ref_type='version')
    command = commands.SetDatasetTagCommand(api_key=api_key)
    command.execute(dataset_version_id, name=name)


@dataset_tags.command("delete", help="Delete dataset tag")
@click.option(
    "--id",
    "dataset_tag_id",
    help="Dataset tag (ex: {}:{})".format(EXAMPLE_ID, EXAMPLE_TAG),
    cls=common.GradientOption,
    required=True,
)
@common.api_key_option
@common.options_file
def delete_dataset_tag(
        dataset_tag_id,
        api_key,
        options_file,
):
    validate_dataset_id(dataset_tag_id, ref_type='tag')
    command = commands.DeleteDatasetTagCommand(api_key=api_key)
    command.execute(dataset_tag_id)


@datasets.group("versions", help="Manage versions", cls=ClickGroup)
def dataset_versions():
    pass


@dataset_versions.command("list", help="List dataset versions")
@click.option(
    "--id",
    "dataset_id",
    help="Dataset ID (ex: {})".format(EXAMPLE_ID),
    cls=common.GradientOption,
    required=True,
)
@click.option(
    "--isCommitted",
    "is_committed",
    type=bool,
    help="Show filter by committed status",
    cls=common.GradientOption,
    default=True,
)
@api_key_option
@common.options_file
def list_dataset_versions(api_key, dataset_id, is_committed, options_file):
    validate_dataset_id(dataset_id)
    command = commands.ListDatasetVersionsCommand(api_key=api_key)
    execute_list(command, dataset_id=dataset_id, is_committed=is_committed)


@dataset_versions.command("details", help="Show dataset version details")
@click.option(
    "--id",
    "dataset_version_id",
    help="Dataset version ID (ex: {}:{})".format(EXAMPLE_ID, EXAMPLE_VERSION),
    cls=common.GradientOption,
    required=True,
)
@api_key_option
@common.options_file
def show_dataset_version_details(api_key, dataset_version_id, options_file):
    validate_dataset_id(dataset_version_id, ref_type='version')
    command = commands.ShowDatasetVersionDetailsCommand(api_key=api_key)
    command.execute(dataset_version_id)


@dataset_versions.command("create", help="Create dataset version")
@click.option(
    "--id",
    "dataset_id",
    help="Dataset version ID (ex: {}:{})".format(EXAMPLE_ID, EXAMPLE_VERSION),
    cls=common.GradientOption,
    required=True,
)
@click.option(
    "--message",
    "message",
    help="Dataset version message",
    cls=common.GradientOption,
)
@click.option(
    "--source-path",
    "source_paths",
    help="Files to put into dataset version (setting this will commit the version)",
    cls=common.GradientOption,
    multiple=True,
)
@common.api_key_option
@common.options_file
def create_dataset_version(
        dataset_id,
        message,
        api_key,
        source_paths,
        options_file,
):
    validate_dataset_id(dataset_id)
    command = commands.CreateDatasetVersionCommand(api_key=api_key)
    command.execute(dataset_id=dataset_id, message=message,
                    source_paths=source_paths)


@dataset_versions.command("update", help="Update dataset version")
@click.option(
    "--id",
    "dataset_version_id",
    help="Dataset version ID (ex: {}:{})".format(EXAMPLE_ID, EXAMPLE_VERSION),
    cls=common.GradientOption,
    required=True,
)
@click.option(
    "--message",
    "message",
    help="Dataset version message",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def update_dataset_version(
        dataset_version_id,
        message,
        api_key,
        options_file,
):
    validate_dataset_id(dataset_version_id, ref_type='version')
    command = commands.UpdateDatasetVersionCommand(api_key=api_key)
    command.execute(dataset_version_id, message=message)


@dataset_versions.command("commit", help="Commit dataset version")
@click.option(
    "--id",
    "dataset_version_id",
    help="Dataset version ID (ex: {}:{})".format(EXAMPLE_ID, EXAMPLE_VERSION),
    cls=common.GradientOption,
    required=True,
)
@common.api_key_option
@common.options_file
def commit_dataset_version(
        dataset_version_id,
        api_key,
        options_file,
):
    validate_dataset_id(dataset_version_id, ref_type='version')
    command = commands.CommitDatasetVersionCommand(api_key=api_key)
    command.execute(dataset_version_id)


@dataset_versions.command("delete", help="Delete dataset version")
@click.option(
    "--id",
    "dataset_version_id",
    help="Dataset version ID (ex: {}:{})".format(EXAMPLE_ID, EXAMPLE_VERSION),
    cls=common.GradientOption,
    required=True,
)
@common.api_key_option
@common.options_file
def delete_dataset_version(dataset_version_id, api_key, options_file):
    validate_dataset_id(dataset_version_id, ref_type='version')
    command = commands.DeleteDatasetVersionCommand(api_key=api_key)
    command.execute(dataset_version_id)


@datasets.group("files", help="Manage files", cls=ClickGroup)
def dataset_version_files():
    pass


@dataset_version_files.command("list", help="List files")
@click.option(
    "--id",
    "dataset_version_id",
    help="Dataset version ID (ex: {}:{})".format(EXAMPLE_ID, EXAMPLE_VERSION),
    cls=common.GradientOption,
    required=True,
)
@click.option(
    "--path",
    "path",
    help="Sub-directory to list",
    cls=common.GradientOption,
)
@click.option(
    "--recursive",
    "recursive",
    help="Recursive list content",
    cls=common.GradientOption,
    type=bool,
)
@api_key_option
@common.options_file
def list_dataset_files(api_key, dataset_version_id, path, recursive, options_file):
    validate_dataset_id(dataset_version_id, ref_type='version')
    command = commands.ListDatasetFilesCommand(api_key=api_key)
    execute_list(command, dataset_version_id=dataset_version_id,
                 path=path, recursive=recursive)


@dataset_version_files.command("get", help="Get files")
@click.option(
    "--id",
    "dataset_version_id",
    help="Dataset version ID (ex: {}:{})".format(EXAMPLE_ID, EXAMPLE_VERSION),
    cls=common.GradientOption,
    required=True,
)
@click.option(
    "--source-path",
    "source_paths",
    help="File or directory to get",
    cls=common.GradientOption,
    multiple=True,
)
@click.option(
    "--target-path",
    "target_path",
    help="Target directory path",
    cls=common.GradientOption,
    required=True,
)
@api_key_option
@common.options_file
def get_dataset_files(api_key, dataset_version_id, source_paths, target_path, options_file):
    validate_dataset_id(dataset_version_id, ref_type='version')
    command = commands.GetDatasetFilesCommand(api_key=api_key)
    command.execute(dataset_version_id=dataset_version_id,
                    source_paths=source_paths, target_path=target_path)


@dataset_version_files.command("put", help="Put files")
@click.option(
    "--id",
    "dataset_version_id",
    help="Dataset version ID (ex: {}:{})".format(EXAMPLE_ID, EXAMPLE_VERSION),
    cls=common.GradientOption,
    required=True,
)
@click.option(
    "--source-path",
    "source_paths",
    help="File or directory to put",
    cls=common.GradientOption,
    multiple=True,
    required=True,
)
@click.option(
    "--target-path",
    "target_path",
    help="Target dataset file path",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def put_dataset_files(api_key, dataset_version_id, source_paths, target_path, options_file):
    validate_dataset_id(dataset_version_id, ref_type='version')
    command = commands.PutDatasetFilesCommand(api_key=api_key)
    command.execute(dataset_version_id=dataset_version_id,
                    source_paths=source_paths, target_path=target_path)


@dataset_version_files.command("delete", help="Delete files")
@click.option(
    "--id",
    "dataset_version_id",
    help="Dataset version ID (ex: {}:{})".format(EXAMPLE_ID, EXAMPLE_VERSION),
    cls=common.GradientOption,
    required=True,
)
@click.option(
    "--path",
    "paths",
    help="Sub-directory to delete",
    cls=common.GradientOption,
    multiple=True,
)
@api_key_option
@common.options_file
def delete_dataset_files(api_key, dataset_version_id, paths, options_file):
    validate_dataset_id(dataset_version_id, ref_type='version')
    command = commands.DeleteDatasetFilesCommand(api_key=api_key)
    command.execute(dataset_version_id=dataset_version_id,
                    paths=paths or ['/'])
