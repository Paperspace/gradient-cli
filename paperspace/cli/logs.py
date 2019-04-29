import click

from paperspace import client, config
from paperspace.cli import common
from paperspace.commands import logs as logs_commands


@click.group("logs", help="Manage gradient logs")
def logs_group():
    pass


@logs_group.command("list", help="List job logs")
@click.option(
    "--jobId",
    "job_id",
    required=True
)
@common.api_key_option
def list_logs(job_id, api_key=None):
    logs_api = client.API(config.CONFIG_LOG_HOST, api_key=api_key)
    command = logs_commands.ListLogsCommand(api=logs_api)
    command.execute(job_id)
