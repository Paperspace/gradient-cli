import os
import sys

import click

from paperspace import client, config
from paperspace.cli import common
from paperspace.cli.cli import cli
from paperspace.cli.common import del_if_value_is_none
from paperspace.cli.jobs import common_jobs_create_options
from paperspace.commands.jobs import CreateJobCommand
from paperspace.workspace import WorkspaceHandler

RUN_MODE_DEFAULT = 1
RUN_MODE_PYTHON_COMMAND = 2
RUN_MODE_SHELL_COMMAND = 3
RUN_MODE_PYTHON_MODULE = 4


def get_executor(mode, python_version=None):
    python_version = python_version or str(sys.version_info[0])  # defaults locally running version
    python_bin = 'python{v}'.format(v=python_version)
    executors = {
        RUN_MODE_DEFAULT: python_bin,
        RUN_MODE_PYTHON_COMMAND: '{python} -c'.format(python=python_bin),
        RUN_MODE_SHELL_COMMAND: '',
        RUN_MODE_PYTHON_MODULE: '{python} -m'.format(python=python_bin),
    }
    return executors[mode]


def clear_script_name(script_name, mode):
    if mode == RUN_MODE_DEFAULT:
        return os.path.basename(script_name)
    return script_name


def create_command(mode, script, python_version=None):
    executor = get_executor(mode, python_version)
    script_name = clear_script_name(script[0], mode)
    script_params = ' '.join(script[1:])
    command = '{executor} {script_name} {script_params}'.format(executor=executor, script_name=script_name,
                                                                script_params=script_params)
    return command


@cli.command("new-run")
@click.option("-c", "--python-command", "mode", flag_value=RUN_MODE_PYTHON_COMMAND)
@click.option("-m", "--module", "mode", flag_value=RUN_MODE_PYTHON_MODULE)
@click.option("-s", "--shell", "mode", flag_value=RUN_MODE_SHELL_COMMAND)
@common_jobs_create_options
@click.argument("script", nargs=-1)
@common.api_key_option
def run(script, api_key, mode, **kwargs):
    del_if_value_is_none(kwargs)

    mode = mode or RUN_MODE_DEFAULT
    command = create_command(mode, script)
    kwargs['command'] = command

    jobs_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = CreateJobCommand(api=jobs_api, workspace_handler=WorkspaceHandler())
    command.execute(kwargs)
