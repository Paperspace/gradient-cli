import functools

import click

from gradient import utils, logger
from gradient.api_sdk.clients import http_client, JobsClient
from gradient.api_sdk.workspace import WorkspaceHandler
from gradient.cli.cli import cli
from gradient.cli.cli_types import json_string
from gradient.cli.common import api_key_option, del_if_value_is_none, ClickGroup, jsonify_dicts, deprecated
from gradient.commands import jobs as jobs_commands
from gradient.config import config


def get_job_client(api_key):
    job_client = JobsClient(
        api_key=api_key,
        logger=logger.Logger(),
        api_url=config.CONFIG_HOST,
        workspace_handler_cls=WorkspaceHandler
    )
    return job_client


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
    job_client = get_job_client(api_key)
    command = jobs_commands.DeleteJobCommand(job_client=job_client)
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
    job_client = get_job_client(api_key)
    command = jobs_commands.StopJobCommand(job_client=job_client)
    command.execute(job_id)


@jobs_group.command("list", help="List jobs with optional filtering")
@click.option(
    "--project",
    "project",
    help="Use to filter jobs by project name",
)
@click.option(
    "--projectId",
    "projectId",
    help="Use to filter jobs by project ID",
)
@click.option(
    "--experimentId",
    "experimentId",
    help="Use to filter jobs by experiment ID",
)
@api_key_option
def list_jobs(api_key, **filters):
    del_if_value_is_none(filters)
    job_client = get_job_client(api_key)
    command = jobs_commands.ListJobsCommand(job_client=job_client)
    command.execute(filters=filters)


def common_jobs_create_options(f):
    options = [
        click.option("--name", "name", help="Job name", required=True),
        click.option("--machineType", "machine_type", help="Virtual machine type"),
        click.option("--container", "container", default="paperspace/tensorflow-python", help="Docker container"),
        click.option("--command", "command", help="Job command/entrypoint"),
        click.option("--ports", "ports", help="Mapped ports"),
        click.option("--isPublic", "is_public", help="Flag: is job public"),
        click.option("--workspace", "workspace", required=False, help="Path to workspace directory"),
        click.option("--workspaceArchive", "workspace_archive", required=False, help="Path to workspace archive"),
        click.option("--workspaceUrl", "workspace_url", required=False, help="Project git repository url"),
        click.option("--workingDirectory", "working_directory", help="Working directory for the experiment", ),
        click.option("--ignoreFiles", "ignore_files", help="Ignore certain files from uploading"),
        click.option("--experimentId", "experiment_id", help="Experiment Id"),
        click.option("--jobEnv", "job_env", type=json_string, help="Environmental variables "),
        click.option("--useDockerfile", "use_dockerfile", help="Flag: using Dockerfile"),
        click.option("--isPreemptible", "is_preemptible", help="Flag: isPreemptible"),
        click.option("--project", "project", help="Project name"),
        click.option("--projectId", "project_id", help="Project ID"),
        click.option("--startedByUserId", "started_by_user_id", help="User ID"),
        click.option("--relDockerfilePath", "rel_dockerfile_path", help="Relative path to Dockerfile"),
        click.option("--registryUsername", "registry_username", help="Docker registry username"),
        click.option("--registryPassword", "registry_password", help="Docker registry password"),
        click.option("--cluster", "cluster", help="Cluster name"),
        click.option("--clusterId", "cluster_id", help="Cluster id"),
        click.option("--nodeAttrs", "node_attrs", type=json_string, help="Cluster node details"),
    ]
    return functools.reduce(lambda x, opt: opt(x), reversed(options), f)


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

    job_client = get_job_client(api_key)
    command = jobs_commands.CreateJobCommand(job_client=job_client)
    job = command.execute(kwargs)
    if job is not None:
        ctx.invoke(list_logs, job_id=job["handle"], line=0, limit=100, follow=True, api_key=api_key)


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
    logs_api = http_client.API(config.CONFIG_LOG_HOST, api_key=api_key)
    command = jobs_commands.JobLogsCommand(api=logs_api)
    command.execute(job_id, line, limit, follow)


@jobs_group.group("artifacts", help="Manage jobs' artifacts", cls=ClickGroup)
def artifacts():
    pass


@artifacts.command("destroy", help="Destroy job's artifacts")
@click.argument("job_id")
@click.option("--files", "files")
@api_key_option
def destroy_artifacts(job_id, api_key=None, files=None):
    jobs_api = http_client.API(config.CONFIG_HOST, api_key=api_key)
    command = jobs_commands.ArtifactsDestroyCommand(api=jobs_api)
    command.execute(job_id, files=files)


@artifacts.command("get", help="Get job's artifacts")
@click.argument("job_id")
@api_key_option
def get_artifacts(job_id, api_key=None):
    jobs_api = http_client.API(config.CONFIG_HOST, api_key=api_key)
    command = jobs_commands.ArtifactsGetCommand(api=jobs_api)
    command.execute(job_id)


@artifacts.command("list", help="List job's artifacts")
@click.argument("job_id")
@click.option("--size", "-s", "size", help="Show file size", is_flag=True)
@click.option("--links", "-l", "links", help="Show file URL", is_flag=True)
@click.option("--files", "files", help="Get only given file (use at the end * as a wildcard)")
@api_key_option
def list_artifacts(job_id, size, links, files, api_key=None):
    jobs_api = http_client.API(config.CONFIG_HOST, api_key=api_key)
    command = jobs_commands.ArtifactsListCommand(api=jobs_api)
    command.execute(job_id=job_id, size=size, links=links, files=files)
