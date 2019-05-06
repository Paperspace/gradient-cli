import click

from paperspace import client, config
from paperspace.cli import common
from paperspace.commands import jobs as jobs_commands


@click.group("jobs", help="Manage gradient jobs", cls=common.ClickGroup)
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
    command.execute(filters)


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
