import sys

import mock
from click.testing import CliRunner

from gradient.cli import cli
from gradient.client import default_headers
from tests import MockResponse


class TestRunCommand(object):
    command_name = 'run'
    common_commands = ["--name", "test", "--projectId", "projectId", "--apiKey", "some_key"]
    url = "https://api.paperspace.io/jobs/createJob/"
    headers = default_headers.copy()
    headers["X-API-Key"] = "some_key"

    @mock.patch("gradient.client.requests.post")
    @mock.patch("gradient.workspace.WorkspaceHandler._zip_workspace")
    @mock.patch("gradient.workspace.MultipartEncoder.get_monitor")
    @mock.patch("gradient.commands.jobs.CreateJobCommand._get_files_dict")
    def test_run_simple_file_with_args(self, get_files_patched, get_moniror_patched, workspace_zip_patched, post_patched):
        get_files_patched.return_value = mock.MagicMock()
        workspace_zip_patched.return_value = '/foo/bar'
        post_patched.return_value = MockResponse(status_code=200)

        mock_monitor = mock.MagicMock()
        mock_monitor.content_type = "mock/multipart"

        get_moniror_patched.return_value = mock_monitor

        runner = CliRunner()
        result = runner.invoke(cli.cli, [self.command_name] + self.common_commands + ["/myscript.py", "a", "b"])

        expected_headers = self.headers.copy()
        expected_headers.update({
            'Content-Type': "mock/multipart"
        })
        post_patched.assert_called_with(self.url,
                                        params={'name': u'test', 'projectId': u'projectId',
                                                'workspaceFileName': 'bar',
                                                'command': 'python{} myscript.py a b'.format(str(sys.version_info[0])),
                                                'container': u'paperspace/tensorflow-python'},
                                        data=mock.ANY,
                                        files=None,
                                        headers=expected_headers,
                                        json=None)

    @mock.patch("gradient.client.requests.post")
    def test_run_python_command_with_args_and_no_workspace(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        runner = CliRunner()
        result = runner.invoke(cli.cli,
                               [self.command_name] + self.common_commands + ["-c", "print(foo)", "--workspace", "none"])

        expected_headers = self.headers.copy()
        post_patched.assert_called_with(self.url,
                                        params={'name': u'test', 'projectId': u'projectId',
                                                'workspaceFileName': 'none',
                                                'workspace': 'none',
                                                'command': 'python{} -c print(foo)'.format(str(sys.version_info[0])),
                                                'container': u'paperspace/tensorflow-python'},
                                        data=None,
                                        files=None,
                                        headers=expected_headers,
                                        json=None)

    @mock.patch("gradient.client.requests.post")
    @mock.patch("gradient.workspace.WorkspaceHandler._zip_workspace")
    def test_run_shell_command_with_args_with_s3_workspace(self, workspace_zip_patched, post_patched):
        workspace_zip_patched.return_value = '/foo/bar'
        post_patched.return_value = MockResponse(status_code=200)

        runner = CliRunner()
        result = runner.invoke(cli.cli,
                               [self.command_name] + self.common_commands + ["-s", "echo foo", "--workspaceUrl",
                                                                             "s3://bucket/object"])

        expected_headers = self.headers.copy()
        post_patched.assert_called_with(self.url,
                                        params={'name': u'test', 'projectId': u'projectId',
                                                'workspaceFileName': 's3://bucket/object',
                                                'workspaceUrl': 's3://bucket/object',
                                                'command': 'echo foo',
                                                'container': u'paperspace/tensorflow-python'},
                                        data=None,
                                        files=None,
                                        headers=expected_headers,
                                        json=None)
