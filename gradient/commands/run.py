import os
import sys

from gradient.api_sdk.constants import RunMode
from gradient.clilogger import CliLogger
from gradient.commands.jobs import RunJobCommand
from gradient.api_sdk.workspace import WorkspaceHandler


class RunCommand(object):

    def __init__(self, api_key=None, logger_=CliLogger()):
        self.api_key = api_key
        self.logger = logger_

    @staticmethod
    def _get_executor(mode, python_version=None):
        python_version = python_version or str(sys.version_info[0])  # defaults locally running version
        python_bin = 'python{v}'.format(v=python_version)
        executors = {
            RunMode.RUN_MODE_DEFAULT: python_bin,
            RunMode.RUN_MODE_PYTHON_COMMAND: '{python} -c'.format(python=python_bin),
            RunMode.RUN_MODE_SHELL_COMMAND: '',
            RunMode.RUN_MODE_PYTHON_MODULE: '{python} -m'.format(python=python_bin),
        }
        return executors[mode]

    @staticmethod
    def _clear_script_name(script_name, mode):
        if mode == RunMode.RUN_MODE_DEFAULT:
            return os.path.basename(script_name)
        return script_name

    def _create_command(self, mode, script, python_version=None):
        command_parts = []
        executor = self._get_executor(mode, python_version)
        if executor:
            command_parts.append(executor)

        script_name = self._clear_script_name(script[0], mode)
        if script_name:
            command_parts.append(script_name)

        script_params = ' '.join(script[1:])
        if script_params:
            command_parts.append(script_params)

        command = ' '.join(command_parts)
        return command

    def execute(self, mode=None, script=None, **json_):
        mode = mode or RunMode.RUN_MODE_DEFAULT
        command = self._create_command(mode, script)
        json_['command'] = command

        command = RunJobCommand(api_key=self.api_key, workspace_handler=WorkspaceHandler(logger_=CliLogger()))
        command.execute(json_)
