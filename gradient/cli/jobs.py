from functools import reduce

import click

from gradient import utils, logger
from gradient.workspace import WorkspaceHandler
from gradient.cli.cli import cli
from gradient.cli.cli_types import json_string
from gradient.cli.common import api_key_option, del_if_value_is_none, ClickGroup, jsonify_dicts, deprecated
from gradient.commands import jobs as jobs_commands


def get_workspace_handler():
    logger_ = logger.Logger()
    workspace_handler = WorkspaceHandler(logger_=logger_)
    return workspace_handler


@cli.group("jobs", help="Manage gradient jobs", cls=ClickGroup)
def jobs_group():
    pass


@jobs_group.command("delete", help="Delete job")
@click.option(
    "--jobId",
    "job_id",
    required=True,
    help="Delete job with given ID",
)
@api_key_option
def delete_job(job_id, api_key=None):
    command = jobs_commands.DeleteJobCommand(api_key=api_key)
    command.execute(job_id)


@jobs_group.command("stop", help="Stop running job")
@click.option(
    "--jobId",
    "job_id",
    required=True,
    help="Stop job with given ID",
)
@api_key_option
def stop_job(job_id, api_key=None):
    command = jobs_commands.StopJobCommand(api_key=api_key)
    command.execute(job_id)


@jobs_group.command("list", help="List jobs with optional filtering")
@click.option(
    "--project",
    "project",
    help="Use to filter jobs by project name",
)
@click.option(
    "--projectId",
    "project_id",
    help="Use to filter jobs by project ID",
)
@click.option(
    "--experimentId",
    "experiment_id",
    help="Use to filter jobs by experiment ID",
)
@api_key_option
def list_jobs(api_key, **filters):
    del_if_value_is_none(filters)

    command = jobs_commands.ListJobsCommand(api_key=api_key)
    command.execute(**filters)


def common_jobs_create_options(f):
    options = [
        click.option("--name", "name", help="Job name"),
        click.option("--machineType", "machine_type", help="Virtual machine type",
                     required=True),
        click.option("--container", "container", default="paperspace/tensorflow-python", help="Docker container",
                     required=True),
        click.option("--command", "command", help="Job command/entrypoint"),
        click.option("--ports", "ports", help="Mapped ports"),
        click.option("--isPublic", "is_public", help="Flag: is job public"),
        click.option("--workspace", "workspace", help="Path to workspace directory"),
        click.option("--workspaceArchive", "workspace_archive", help="Path to workspace archive"),
        click.option("--workspaceUrl", "workspace_url", help="Project git repository url"),
        click.option("--workingDirectory", "working_directory", help="Working directory for the experiment",),
        click.option("--ignoreFiles", "ignore_files", help="Ignore certain files from uploading"),
        click.option("--experimentId", "experiment_id", help="Experiment Id"),
        click.option("--jobEnv", "job_env", type=json_string, help="Environmental variables "),
        click.option("--useDockerfile", "use_dockerfile", help="Flag: using Dockerfile"),
        click.option("--isPreemptible", "is_preemptible", help="Flag: isPreemptible"),
        click.option("--project", "project", help="Project name"),
        click.option("--projectId", "project_id", help="Project ID", required=True),
        click.option("--startedByUserId", "started_by_user_id", help="User ID"),
        click.option("--relDockerfilePath", "rel_dockerfile_path", help="Relative path to Dockerfile"),
        click.option("--registryUsername", "registry_username", help="Docker registry username"),
        click.option("--registryPassword", "registry_password", help="Docker registry password"),
        click.option("--cluster", "cluster", help="Cluster name"),
        click.option("--clusterId", "cluster_id", help="Cluster id"),
        click.option("--nodeAttrs", "node_attrs", type=json_string, help="Cluster node details"),
    ]
    return reduce(lambda x, opt: opt(x), reversed(options), f)


@deprecated("DeprecatedWarning: \nWARNING: --workspaceUrl and --workspaceArchive "
            "options will not be included in version 0.6.0")
@jobs_group.command("create", help="Create job")
@common_jobs_create_options
@api_key_option
@click.pass_context
def create_job(ctx, api_key, **kwargs):
    utils.validate_workspace_input(kwargs)
    del_if_value_is_none(kwargs)
    jsonify_dicts(kwargs)

    command = jobs_commands.CreateJobCommand(api_key=api_key, workspace_handler=get_workspace_handler())
    job_handle = command.execute(kwargs)
    if job_handle is not None:
        ctx.invoke(list_logs, job_id=job_handle, line=0, limit=100, follow=True, api_key=api_key)


@jobs_group.command("logs", help="List job logs")
@click.option(
    "--jobId",
    "job_id",
    required=True
)
@click.option(
    "--line",
    "line",
    required=False,
    default=0
)
@click.option(
    "--limit",
    "limit",
    required=False,
    default=10000
)
@click.option(
    "--follow",
    "follow",
    required=False,
    default=False
)
@api_key_option
def list_logs(job_id, line, limit, follow, api_key=None):
    command = jobs_commands.JobLogsCommand(api_key=api_key)
    command.execute(job_id, line, limit, follow)


@jobs_group.group("artifacts", help="Manage jobs' artifacts", cls=ClickGroup)
def artifacts():
    pass


@artifacts.command("destroy", help="Destroy job's artifacts")
@click.argument("job_id")
@click.option("--files", "files")
@api_key_option
def destroy_artifacts(job_id, api_key=None, files=None):
    command = jobs_commands.ArtifactsDestroyCommand(api_key=api_key)
    command.execute(job_id, files=files)


@artifacts.command("get", help="Get job's artifacts")
@click.argument("job_id")
@api_key_option
def get_artifacts(job_id, api_key=None):
    command = jobs_commands.ArtifactsGetCommand(api_key=api_key)
    command.execute(job_id)


@artifacts.command("list", help="List job's artifacts")
@click.argument("job_id")
@click.option("--size", "-s", "size", help="Show file size", is_flag=True)
@click.option("--links", "-l", "links", help="Show file URL", is_flag=True, default=False)
@click.option("--files", "files", help="Get only given file (use at the end * as a wildcard)")
@api_key_option
def list_artifacts(job_id, size, links, files, api_key=None):
    command = jobs_commands.ArtifactsListCommand(api_key=api_key)
    command.execute(job_id=job_id, size=size, links=links, files=files)
