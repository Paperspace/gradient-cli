import click

from paperspace import client, config
from paperspace.cli import common
from paperspace.cli.cli_types import json_string
from paperspace.cli.common import del_if_value_is_none, ClickGroup
from paperspace.cli.cli import cli
from paperspace.commands import jobs as jobs_commands


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
@common.api_key_option
def delete_job(job_id, api_key=None):
    jobs_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = jobs_commands.DeleteJobCommand(api=jobs_api)
    command.execute(job_id)


@jobs_group.command("stop", help="Stop running job")
@click.option(
    "--jobId",
    "job_id",
    required=True,
    help="Stop job with given ID",
)
@common.api_key_option
def stop_job(job_id, api_key=None):
    jobs_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = jobs_commands.StopJobCommand(api=jobs_api)
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
@common.api_key_option
def list_jobs(api_key, **filters):
    common.del_if_value_is_none(filters)
    jobs_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = jobs_commands.ListJobsCommand(api=jobs_api)
    command.execute(filters=filters)


@jobs_group.command("create", help="Create job")
@click.option("--name", "name", help="Job name", required=True)
@click.option("--machineType", "machineType", help="Virtual machine type")
@click.option("--container", "container", help="Docker container")
@click.option("--command", "command", help="Job command/entrypoint")
@click.option("--ports", "ports", help="Mapped ports")
@click.option("--isPublic", "isPublic", help="Flag: is job public")
@click.option("--workspace", "workspace", required=False, help="Path to workspace directory")
@click.option("--workspaceArchive", "workspaceArchive", required=False, help="Path to workspace archive")
@click.option("--workspaceUrl", "workspaceUrl", required=False, help="Project git repository url")
@click.option("--workingDirectory", "workingDirectory", help="Working directory for the experiment", )
@click.option("--experimentId", "experimentId", help="Experiment Id")
@click.option("--jobEnv", "envVars", type=json_string, help="Environmental variables ")
@click.option("--useDockerfile", "useDockerfile", help="Flag: using Dockerfile")
@click.option("--isPreemptible", "isPreemptible", help="Flag: isPreemptible")
@click.option("--project", "project", help="Project name")
@click.option("--projectId", "projectHandle", help="Project ID", required=True)
@click.option("--startedByUserId", "startedByUserId", help="User ID")
@click.option("--relDockerfilePath", "relDockerfilePath", help="Relative path to Dockerfile")
@click.option("--registryUsername", "registryUsername", help="Docker registry username")
@click.option("--registryPassword", "registryPassword", help="Docker registry password")
@common.api_key_option
def create_job(api_key, **kwargs):
    del_if_value_is_none(kwargs)
    jobs_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = jobs_commands.CreateJobCommand(api=jobs_api)
    command.execute(kwargs)


@jobs_group.command("log", help="List job logs")
@click.option(
    "--jobId",
    "job_id",
    required=True
)
@common.api_key_option
def list_logs(job_id, api_key=None):
    logs_api = client.API(config.CONFIG_LOG_HOST, api_key=api_key)
    command = jobs_commands.JobLogsCommand(api=logs_api)
    command.execute(job_id)
