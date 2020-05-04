import sys

import mock
from click.testing import CliRunner

from gradient.api_sdk.clients.http_client import default_headers
from gradient.cli import cli
from tests import MockResponse

EXPECTED_HEADERS = default_headers.copy()
EXPECTED_HEADERS["ps_client_name"] = "gradient-cli"

EXPECTED_HEADERS_WITH_CHANGED_API_KEY = EXPECTED_HEADERS.copy()
EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"


class TestRunCommand(object):
    command_name = 'run'
    common_commands = [
        "--name", "test", "--projectId", "projectId", "--apiKey", "some_key", "--machineType", "G1",
    ]
    COMMAND_WITH_OPTIONS_FILE = ["run", "--optionsFile", ]  # path added in test

    url = "https://api.paperspace.io/jobs/createJob/"
    headers = EXPECTED_HEADERS_WITH_CHANGED_API_KEY.copy()
    headers["X-API-Key"] = "some_key"

    RESPONSE_JSON_200 = {"id": "sadkfhlskdjh", "message": "success"}
    RESPONSE_CONTENT_200 = b'{"handle":"sadkfhlskdjh","message":"success"}\n'

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    @mock.patch("gradient.api_sdk.workspace.WorkspaceHandler._zip_workspace")
    @mock.patch("gradient.api_sdk.utils.MultipartEncoder.get_monitor")
    @mock.patch("gradient.commands.jobs.CreateJobCommand._get_files_dict")
    def test_run_simple_file_with_args(self, get_files_patched, get_moniror_patched, workspace_zip_patched,
                                       post_patched):
        get_files_patched.return_value = mock.MagicMock()
        workspace_zip_patched.return_value = '/foo/bar'
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)

        mock_monitor = mock.MagicMock()
        mock_monitor.content_type = "mock/multipart"

        get_moniror_patched.return_value = mock_monitor

        runner = CliRunner()
        command = [self.command_name] + self.common_commands + ["/myscript.py", "a", "b"]
        result = runner.invoke(cli.cli, command)

        expected_headers = self.headers.copy()
        expected_headers.update({
            'Content-Type': "mock/multipart"
        })
        assert result.exit_code == 0, result.exc_info
        post_patched.assert_called_with(self.url,
                                        json=None,
                                        data=mock.ANY,
                                        files=None,
                                        headers=expected_headers,
                                        params={
                                            'name': u'test',
                                            'projectId': u'projectId',
                                            'workspaceFileName': 'bar',
                                            'command': 'python{} myscript.py a b'.format(str(sys.version_info[0])),
                                            'container': u'paperspace/tensorflow-python',
                                            'machineType': 'G1',
                                        })

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_run_python_command_with_args_and_no_workspace(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        runner = CliRunner()
        result = runner.invoke(cli.cli,
                               [self.command_name] + self.common_commands + ["-c", "print(foo)", "--workspace", "none"])

        expected_headers = self.headers.copy()
        post_patched.assert_called_with(self.url,
                                        json=None,
                                        data=None,
                                        files=None,
                                        headers=expected_headers,
                                        params={
                                            'name': u'test',
                                            'projectId': u'projectId',
                                            'workspaceFileName': 'none',
                                            'command': 'python{} -c print(foo)'.format(str(sys.version_info[0])),
                                            'container': u'paperspace/tensorflow-python',
                                            'machineType': 'G1',
                                        })

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    @mock.patch("gradient.api_sdk.workspace.WorkspaceHandler._zip_workspace")
    def test_run_shell_command_with_args_with_s3_workspace(self, workspace_zip_patched, post_patched):
        workspace_zip_patched.return_value = '/foo/bar'
        post_patched.return_value = MockResponse()

        runner = CliRunner()
        result = runner.invoke(cli.cli,
                               [self.command_name] + self.common_commands + ["-s", "echo foo", "--workspace",
                                                                             "s3://bucket/object"])

        expected_headers = self.headers.copy()
        post_patched.assert_called_with(self.url,
                                        json=None,
                                        data=None,
                                        files=None,
                                        headers=expected_headers,
                                        params={
                                            'name': u'test',
                                            'projectId': u'projectId',
                                            'workspaceFileName': 's3://bucket/object',
                                            'command': 'echo foo',
                                            'container': u'paperspace/tensorflow-python',
                                            'machineType': 'G1',
                                        })

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    @mock.patch("gradient.api_sdk.workspace.WorkspaceHandler._zip_workspace")
    def test_should_read_options_from_yaml_file(self, workspace_zip_patched, post_patched, run_config_path):
        workspace_zip_patched.return_value = '/foo/bar'
        post_patched.return_value = MockResponse()
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [run_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        expected_headers = self.headers.copy()
        post_patched.assert_called_with(self.url,
                                        json=None,
                                        data=None,
                                        files=None,
                                        headers=expected_headers,
                                        params={'useDockerfile': True,
                                                'machineType': 'some_machine_type',
                                                'name': 'some_name',
                                                'workingDirectory': '/some/directory',
                                                'relDockerfilePath': '/some/dockerfile/path',
                                                'isPreemptible': True,
                                                'projectId': 'some_project_id',
                                                'registryTargetPassword': 'some_registry_target_password',
                                                'isPublic': True,
                                                'clusterId': 'some_cluster_id',
                                                'command': 'some_script.py some_other_script.py',
                                                'experimentId': 'some_experiment_id',
                                                'workspaceFileName': 's3://bucket/object',
                                                'targetNodeAttrs': {'key': 'val2'},
                                                'container': 'some_container',
                                                'jobEnv': {'key': 'val'},
                                                'registryTargetUsername': 'some_registry_target_username',
                                                'registryTarget': 'some_registry_target',
                                                'startedByUserId': 'some_user_id',
                                                'ports': '8080,9000:9900',
                                                'registryPassword': 'some_registry_password',
                                                'registryUsername': 'some_registry_username',
                                                })
