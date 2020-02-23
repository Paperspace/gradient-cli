import click

from gradient.api_sdk.constants import RunMode
from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.common import del_if_value_is_none, deprecated, jsonify_dicts
from gradient.cli.jobs import common_jobs_create_options
from gradient.commands.run import RunCommand


@deprecated("DeprecatedWarning: \nWARNING: This command will not be included in version 0.6.0\n")
@cli.command(
    "run",
    help="Run script or command on remote cluster",
)
@click.option(
    "-c",
    "--python-command",
    "mode",
    flag_value=RunMode.RUN_MODE_PYTHON_COMMAND,
    cls=common.GradientOption,
)
@click.option(
    "-m",
    "--module",
    "mode",
    flag_value=RunMode.RUN_MODE_PYTHON_MODULE,
    cls=common.GradientOption,
)
@click.option(
    "-s",
    "--shell",
    "mode",
    flag_value=RunMode.RUN_MODE_SHELL_COMMAND,
    cls=common.GradientOption,
)
@common_jobs_create_options
@click.argument("script", nargs=-1, required=True, cls=common.GradientArgument)
@common.api_key_option
@common.options_file
def run(api_key, options_file, **kwargs):
    del_if_value_is_none(kwargs)
    jsonify_dicts(kwargs)

    command = RunCommand(api_key=api_key)
    command.execute(**kwargs)
