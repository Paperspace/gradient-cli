import click

from paperspace import client, config
from paperspace.cli import common
from paperspace.cli.cli import cli
from paperspace.cli.common import del_if_value_is_none, deprecated, jsonify_dicts
from paperspace.cli.jobs import common_jobs_create_options
from paperspace.commands.run import RunCommand
from paperspace.constants import RunMode


@deprecated(version="0.6.0")
@cli.command("run", help="Run script or command on remote cluster")
@click.option("-c", "--python-command", "mode", flag_value=RunMode.RUN_MODE_PYTHON_COMMAND)
@click.option("-m", "--module", "mode", flag_value=RunMode.RUN_MODE_PYTHON_MODULE)
@click.option("-s", "--shell", "mode", flag_value=RunMode.RUN_MODE_SHELL_COMMAND)
@common_jobs_create_options
@click.argument("script", nargs=-1, required=True)
@common.api_key_option
def run(api_key, **kwargs):
    del_if_value_is_none(kwargs)
    jsonify_dicts(kwargs)

    jobs_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = RunCommand(api=jobs_api)
    command.execute(**kwargs)
