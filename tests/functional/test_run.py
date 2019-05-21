import mock
from click.testing import CliRunner

from paperspace.cli import cli
from paperspace.client import default_headers
from tests import MockResponse


class TestRunCommand(object):
    command_name = 'new-run'
    common_commands = ["--name", "test", "--projectId", "projectId", "--apiKey", "some_key"]
    url = "https://api.paperspace.io/jobs/createJob/"
    headers = default_headers.copy()
    headers["X-API-Key"] = "some_key"

    @mock.patch("paperspace.client.requests.post")
    @mock.patch("paperspace.workspace.WorkspaceHandler._zip_workspace")
    def test_run_simple_file_with_args(self, workspace_zip_patched, post_patched):
        workspace_zip_patched.return_value = '/dev/random'
        post_patched.return_value = MockResponse(status_code=200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, [self.command_name] + self.common_commands + ["/myscript.py", "a", "b"])

        expected_headers = self.headers.copy()
        expected_headers.update({
            'Content-Type': "multipart/form-data"
        })
        post_patched.assert_called_with(self.url,
                                        params={'name': u'test', 'projectId': u'projectId',
                                                'workspaceFileName': 'random',
                                                'command': 'python2 myscript.py a b',
                                                'projectHandle': u'projectId',
                                                'container': u'paperspace/tensorflow-python'},
                                        data=None,
                                        files=mock.ANY,
                                        headers=expected_headers,
                                        json=None)

    @mock.patch("paperspace.client.requests.post")
    @mock.patch("paperspace.workspace.WorkspaceHandler._zip_workspace")
    def test_run_python_command_with_args_and_no_workspace(self, workspace_zip_patched, post_patched):
        workspace_zip_patched.return_value = '/dev/random'
        post_patched.return_value = MockResponse(status_code=200)

        runner = CliRunner()
        result = runner.invoke(cli.cli,
                               [self.command_name] + self.common_commands + ["-c", "print(foo)", "--workspace", "none"])

        expected_headers = self.headers.copy()
        post_patched.assert_called_with(self.url,
                                        params={'name': u'test', 'projectId': u'projectId',
                                                'workspaceFileName': 'none',
                                                'workspace': 'none',
                                                'command': 'python2 -c print(foo)',
                                                'projectHandle': u'projectId',
                                                'container': u'paperspace/tensorflow-python'},
                                        data=None,
                                        files=None,
                                        headers=expected_headers,
                                        json=None)
