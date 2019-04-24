import click

from paperspace import client, config
from paperspace.commands import jobs as jobs_commands


@click.group("jobs", help="Manage gradient jobs")
def jobs_group():
    pass


@jobs_group.command("delete", help="Delete job")
@click.option(
    "--jobId",
    "job_id",
    required=True,
)
def delete_job(job_id, api_key=None):
    jobs_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = jobs_commands.DeleteJobCommand(api=jobs_api)
    command.execute(job_id)
