import click

from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.common import validate_comma_split_option
from gradient.commands import notebooks


@cli.group("notebooks", help="Manage notebooks", cls=common.ClickGroup)
def notebooks_group():
    pass


@notebooks_group.group("tags", help="Manage notebook tags", cls=common.ClickGroup)
def notebook_tags():
    pass


# @notebooks_group.command("create", help="Create new notebook")
# @click.option(
#     "--vmTypeId",
#     "vm_type_id",
#     type=int,
#     required=True,
#     help="Type of Virtual Machine",
#     cls=common.GradientOption,
# )
@click.option(
    "--containerId",
    "container_id",
    type=int,
    required=True,
    help="Container ID",
    cls=common.GradientOption,
)
@click.option(
    "--clusterId",
    "cluster_id",
    type=int,
    required=True,
    help="Cluster ID",
    cls=common.GradientOption,
)
@click.option(
    "--containerName",
    "container_name",
    help="Container name",
    cls=common.GradientOption,
)
@click.option(
    "--name",
    "name",
    help="Notebook name",
    cls=common.GradientOption,
)
@click.option(
    "--registryUsername",
    "registry_username",
    help="Registry username",
    cls=common.GradientOption,
)
@click.option(
    "--registryPassword",
    "registry_password",
    help="Registry password",
    cls=common.GradientOption,
)
@click.option(
    "--defaultEntrypoint",
    "default_entrypoint",
    help="Default entrypoint",
    cls=common.GradientOption,
)
@click.option(
    "--containerUser",
    "container_user",
    help="Container user",
    cls=common.GradientOption,
)
@click.option(
    "--shutdownTimeout",
    "shutdown_timeout",
    help="Shutdown timeout in hours",
    type=float,
    cls=common.GradientOption,
)
@click.option(
    "--isPreemptible",
    "is_preemptible",
    help="Is preemptible",
    is_flag=True,
    type=bool,
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
def create_notebook(api_key, options_file, **notebook):
    notebook["tags"] = validate_comma_split_option(notebook.pop("tags_comma"), notebook.pop("tags"))
    command = notebooks.CreateNotebookCommand(api_key=api_key)
    command.execute(**notebook)


@notebooks_group.command("delete", help="Delete existing notebook")
@click.option(
    "--id",
    "id_",
    help="Notebook ID",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def delete_notebook(id_, api_key, options_file):
    command = notebooks.DeleteNotebookCommand(api_key=api_key)
    command.execute(id_=id_)


@notebooks_group.command("list", help="List notebooks")
@click.option("--limit", "-l", "n_limit", default=20)
@click.option("--offset", "-o", "n_offset", default=0)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    cls=common.GradientOption,
    help="Filter by tags. Multiple use"
)
@common.api_key_option
@common.options_file
def list_notebooks(n_limit, n_offset, tags, api_key, options_file):
    command = notebooks.ListNotebooksCommand(api_key=api_key)
    for notebook_str, next_iteration in command.execute(limit=n_limit, offset=n_offset, tags=tags):
        click.echo(notebook_str)
        if next_iteration:
            click.confirm("Do you want to continue?", abort=True)


@notebooks_group.command("details", help="Show notebook details")
@click.option(
    "--id",
    "id",
    help="Notebook ID",
    cls=common.GradientOption,
    required=True,
)
@common.api_key_option
@common.options_file
def show_notebook(id, api_key, options_file):
    command = notebooks.ShowNotebookDetailsCommand(api_key=api_key)
    command.execute(id)


@notebook_tags.command("add", help="Add tags to notebook")
@click.option(
    "--id",
    "id",
    required=True,
    cls=common.GradientOption,
    help="ID of the notebook",
)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    help="One or many tags that you want to add to notebook",
    cls=common.GradientOption
)
@click.option(
    "--tags",
    "tags_comma",
    help="Separated by comma tags that you want add to notebook",
    cls=common.GradientOption
)
@common.api_key_option
@common.options_file
def notebook_add_tag(id, options_file, api_key, **kwargs):
    kwargs["tags"] = validate_comma_split_option(kwargs.pop("tags_comma"), kwargs.pop("tags"), raise_if_no_tags=True)

    command = notebooks.NotebookAddTagsCommand(api_key=api_key)
    command.execute(id, **kwargs)


@notebook_tags.command("remove", help="Remove tags from notebook")
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
    help="One or many tags that you want to remove from notebook",
    cls=common.GradientOption
)
@click.option(
    "--tags",
    "tags_comma",
    help="Separated by comma tags that you want to remove from notebook",
    cls=common.GradientOption
)
@common.api_key_option
@common.options_file
def notebook_remove_tags(id, options_file, api_key, **kwargs):
    kwargs["tags"] = validate_comma_split_option(kwargs.pop("tags_comma"), kwargs.pop("tags"), raise_if_no_tags=True)

    command = notebooks.NotebookRemoveTagsCommand(api_key=api_key)
    command.execute(id, **kwargs)
