import mock
import pytest
from click.testing import CliRunner

from gradient.api_sdk.clients.http_client import default_headers
from gradient.cli import cli
from tests import example_responses, MockResponse


class TestJobs(object):
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to fetch data: Invalid API token\n"
    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}

    EXPECTED_HEADERS = default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"


class TestListJobs(TestJobs):
    URL = "https://api.paperspace.io/jobs/getJobs/"
    BASIC_COMMAND = ["jobs", "list"]
    COMMAND_WITH_OPTIONS_FILE = ["jobs", "list", "--optionsFile", ]  # path added in test

    EXPECTED_RESPONSE_JSON = example_responses.LIST_JOBS_RESPONSE_JSON
    EXPECTED_STDOUT = """+----------------+---------------------------+-------------------+----------------+--------------+--------------------------+
| ID             | Name                      | Project           | Cluster        | Machine Type | Created                  |
+----------------+---------------------------+-------------------+----------------+--------------+--------------------------+
| jsxeeba5qq99yn | job 1                     | keton             | PS Jobs on GCP | K80          | 2019-03-25T14:51:16.118Z |
| jfl063dsv634h  | job 2                     | keton             | PS Jobs on GCP | P100         | 2019-03-25T14:54:30.866Z |
| jsvau8w47k78zm | Clone - jfl063dsv634h     | keton             | PS Jobs on GCP | P100         | 2019-03-25T15:04:43.844Z |
| j2eq99xhvgtum  | keton1-worker-1           | keton             | PS Jobs on GCP | P100         | 2019-03-25T15:07:30.383Z |
| jzzinybinuxf9  | keton2-worker-1           | keton             | PS Jobs on GCP | P100         | 2019-03-25T15:18:51.461Z |
| jsb37duc1zlbz0 | keton4-worker-1           | keton             | PS Jobs on GCP | P100         | 2019-03-25T15:29:04.601Z |
| jq41vipwy18f7  | keton4-parameter_server-1 | keton             | PS Jobs on GCP | P100         | 2019-03-25T15:29:06.765Z |
| jsigkjnyb6m3qm | Test1-worker-1            | keton             | PS Jobs on GCP | K80          | 2019-04-02T15:17:05.618Z |
| j4g76vuppxqao  | job 1                     | paperspace-python | PS Jobs on GCP | K80          | 2019-04-04T15:12:34.414Z |
| jsbnvdhwb46vr9 | job 2                     | paperspace-python | PS Jobs on GCP | G1           | 2019-04-24T09:09:53.645Z |
| jt8alwzv28kha  | job 3                     | paperspace-python | PS Jobs on GCP | G1           | 2019-04-24T10:18:30.620Z |
+----------------+---------------------------+-------------------+----------------+--------------+--------------------------+
"""

    BASIC_COMMAND_WITH_API_KEY = ["jobs", "list", "--apiKey", "some_key"]

    RESPONSE_JSON_WHEN_NO_JOBS_WERE_FOUND = []
    EXPECTED_STDOUT_WHEN_NO_JOBS_WERE_FOUND = "No data found\n"

    BASIC_COMMAND_WITH_FILTERING = [
        "jobs", "list",
        "--projectId", "some_project_id",
        "--experimentId", "some_experiment_id",
    ]
    EXPECTED_REQUEST_JSON_WITH_FILTERING = {
        "projectId": "some_project_id",
        "experimentId": "some_experiment_id",
    }

    BASIC_COMMAND_WITH_MUTUALLY_EXCLUSIVE_FILTERS = [
        "jobs", "list",
        "--project", "some_project_name",
        "--projectId", "some_project_id",
    ]
    EXPECTED_REQUEST_JSON_WITH_MUTUALLY_EXCLUSIVE_FILTERS = {
        "project": "some_project_name",
        "projectId": "some_project_id",
    }
    RESPONSE_JSON_WITH_MUTUALLY_EXCLUSIVE_FILTERS = {
        "error": {
            "name": "Error",
            "status": 422,
            "message": "Incompatible parameters: project and projectId cannot both be specified",
        },
    }
    EXPECTED_STDOUT_WHEN_MUTUALLY_EXCLUSIVE_FILTERS = "Failed to fetch data: Incompatible parameters: project and " \
                                                      "projectId cannot both be specified\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_and_print_table_when_jobs_list_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_jobs_list_was_used_with_api_key_option(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, get_patched, jobs_list_config_path):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [jobs_list_config_path]

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, command)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=self.EXPECTED_REQUEST_JSON_WITH_FILTERING,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_jobs_list_was_used_with_wrong_api_key(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_error_message_when_no_job_was_not_found(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_NO_JOBS_WERE_FOUND)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT_WHEN_NO_JOBS_WERE_FOUND
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=None)
        assert result.output == "Failed to fetch data\n"
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_jobs_list_was_used_with_filter_options(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_FILTERING)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.EXPECTED_REQUEST_JSON_WITH_FILTERING,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_proper_message_when_jobs_list_was_used_with_mutually_exclusive_filters(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_MUTUALLY_EXCLUSIVE_FILTERS,
                                                status_code=422)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_MUTUALLY_EXCLUSIVE_FILTERS)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.EXPECTED_REQUEST_JSON_WITH_MUTUALLY_EXCLUSIVE_FILTERS,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT_WHEN_MUTUALLY_EXCLUSIVE_FILTERS
        assert result.exit_code == 0


class TestJobLogs(TestJobs):
    URL = "https://logs.paperspace.io/jobs/logs"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_RESPONSE_JSON = example_responses.LIST_OF_LOGS_FOR_JOB
    COMMAND_WITHOUT_REQUIRED_PARAMETERS = ["jobs", "logs"]
    COMMAND_WITH_ALL_OPTIONS = [
        "jobs", "logs",
        "--jobId", "some_id",
        "--apiKey", "some_key",
        "--line", "50",
        "--limit", "200",
        # "--follow", "True",
    ]

    COMMAND_WITH_OPTIONS_FILE = ["jobs", "logs", "--optionsFile", ]  # path added in test
    REQUEST_WITH_OPTIONS_FILE = {"jobId": "some_id", "line": 50, "limit": 200}

    EXPECTED_STDOUT_WITHOUT_PARAMETERS = """Usage: cli jobs logs [OPTIONS]
Try "cli jobs logs --help" for help.

Error: Missing option "--jobId".
"""

    EXPECTED_STDOUT = """+Job some_id logs------------------------------------------------------------------------+
| LINE | MESSAGE                                                                         |
+------+---------------------------------------------------------------------------------+
| 1    | Traceback (most recent call last):                                              |
| 2    |   File "generate_figures.py", line 15, in <module>                              |
| 3    |     import dnnlib.tflib as tflib                                                |
| 4    |   File "/paperspace/dnnlib/tflib/__init__.py", line 8, in <module>              |
| 5    |     from . import autosummary                                                   |
| 6    |   File "/paperspace/dnnlib/tflib/autosummary.py", line 31, in <module>          |
| 7    |     from . import tfutil                                                        |
| 8    |   File "/paperspace/dnnlib/tflib/tfutil.py", line 34, in <module>               |
| 9    |     def shape_to_list(shape: Iterable[tf.Dimension]) -> List[Union[int, None]]: |
| 10   | AttributeError: module \'tensorflow\' has no attribute 'Dimension'                |
| 11   | PSEOF                                                                           |
+------+---------------------------------------------------------------------------------+
"""

    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to fetch data: Invalid API token\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_command_should_not_send_request_without_required_parameters(self, get_patched):
        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITHOUT_REQUIRED_PARAMETERS)

        get_patched.assert_not_called()
        assert result.exit_code == 2
        assert result.output == self.EXPECTED_STDOUT_WITHOUT_PARAMETERS

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_get_request_and_print_available_logs(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITH_ALL_OPTIONS)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_WITH_OPTIONS_FILE)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_get_request_when_log_list_was_used_with_wrong_api_key(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITH_ALL_OPTIONS)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_WITH_OPTIONS_FILE)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, get_patched, jobs_logs_config_path):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [jobs_logs_config_path]

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, command)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_WITH_OPTIONS_FILE)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITH_ALL_OPTIONS)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_WITH_OPTIONS_FILE)
        assert result.output == "Failed to fetch data\n"
        assert result.exit_code == 0


class TestDestroyJobArtifactsCommands(TestJobs):
    runner = CliRunner()
    URL = "https://api.paperspace.io"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_post_request_when_destroying_artifacts_with_files_specified(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)
        job_id = "some_job_id"
        file_names = "some_file_names"
        result = self.runner.invoke(cli.cli, ["jobs", "artifacts", "destroy", job_id, "--files", file_names, "--apiKey",
                                              "some_key"])

        assert result.exit_code == 0, result.exc_info
        post_patched.assert_called_with("{}/jobs/{}/artifactsDestroy/".format(self.URL, job_id),
                                        files=None,
                                        headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params={"files": file_names},
                                        data=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_post_request_when_destroying_artifacts_without_files_specified(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)
        job_id = "some_job_id"
        result = self.runner.invoke(cli.cli, ["jobs", "artifacts", "destroy", job_id, "--apiKey", "some_key"])

        post_patched.assert_called_with("{}/jobs/{}/artifactsDestroy/".format(self.URL, job_id),
                                        files=None,
                                        headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params=None,
                                        data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, post_patched, jobs_artifacts_destroy_config_path):
        post_patched.return_value = MockResponse()
        command = ["jobs", "artifacts", "destroy", "--optionsFile", jobs_artifacts_destroy_config_path]

        result = self.runner.invoke(cli.cli, command)

        assert result.exit_code == 0, result.exc_info
        post_patched.assert_called_with("{}/jobs/some_id/artifactsDestroy/".format(self.URL),
                                        files=None,
                                        headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params={"files": "file1,file2"},
                                        data=None)


class TestGetJobArtifacts(TestJobs):
    runner = CliRunner()
    URL = "https://api.paperspace.io"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_send_valid_get_request_and_receive_json_response(self, get_patched):
        get_patched.return_value = MockResponse()
        job_id = "some_job_id"
        result = self.runner.invoke(cli.cli, ["jobs", "artifacts", "get", job_id, "--apiKey", "some_key"])

        get_patched.assert_called_with("{}/jobs/artifactsGet".format(self.URL),
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params={"jobId": job_id})
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, get_patched, jobs_artifacts_get_config_path):
        get_patched.return_value = MockResponse()
        command = ["jobs", "artifacts", "get", "--optionsFile", jobs_artifacts_get_config_path]

        result = self.runner.invoke(cli.cli, command)

        get_patched.assert_called_with("{}/jobs/artifactsGet".format(self.URL),
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params={"jobId": "some_id"})
        assert result.exit_code == 0


class TestListJobArtifacts(TestJobs):
    runner = CliRunner()
    URL = "https://api.paperspace.io"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_get_request_with_all_parameters_for_a_list_of_artifacts(self, get_patched):
        get_patched.return_value = MockResponse()
        job_id = "some_job_id"
        result = self.runner.invoke(cli.cli,
                                    ["jobs", "artifacts", "list", job_id, "--apiKey", "some_key", "--size", "--links",
                                     "--files", "foo"])

        get_patched.assert_called_with("{}/jobs/artifactsList".format(self.URL),
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params={"jobId": job_id,
                                               "size": True,
                                               "links": True,
                                               "files": "foo"})
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, get_patched, jobs_artifacts_list_config_path):
        get_patched.return_value = MockResponse()
        command = ["jobs", "artifacts", "list", "--optionsFile", jobs_artifacts_list_config_path]
        result = self.runner.invoke(cli.cli, command)

        get_patched.assert_called_with("{}/jobs/artifactsList".format(self.URL),
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params={"files": "keton*.py",
                                               "size": True,
                                               "links": True,
                                               "jobId": "some_id"})
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @pytest.mark.parametrize('option,param', [("--size", "size"),
                                              ("-s", "size"),
                                              ("--links", "links"),
                                              ("-l", "links")])
    def test_should_send_valid_get_request_with_valid_param_for_a_list_of_artifacts_for_both_formats_of_param(self,
                                                                                                              get_patched,
                                                                                                              option,
                                                                                                              param):
        get_patched.return_value = MockResponse(status_code=200)
        job_id = "some_job_id"
        result = self.runner.invoke(cli.cli,
                                    ["jobs", "artifacts", "list", job_id, "--apiKey", "some_key"] + [option])

        get_patched.assert_called_with("{}/jobs/artifactsList".format(self.URL),
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params={"jobId": job_id,
                                               param: True})
        assert result.exit_code == 0


class TestJobsCreate(object):
    URL = "https://api.paperspace.io"
    EXPECTED_HEADERS = default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"
    BASIC_OPTIONS_COMMAND = [
        "jobs", "create",
        "--name", "exp1",
        "--projectId", "testHandle",
        "--container", "testContainer",
        "--machineType", "testType",
        "--command", "testCommand",
        "--workspace", "https://github.com/Paperspace/gradient-cli.git",
    ]
    FULL_OPTIONS_COMMAND = [
        "jobs", "create",
        "--apiKey", "some_key",
        "--cluster", "some_cluster_name",
        "--clusterId", "some_cluster_id",
        "--command", "some command",
        "--container", "some_container",
        "--experimentId", "some_experiment_id",
        "--ignoreFiles", "file1,file2",
        "--isPreemptible", "True",
        "--projectId", "some_project_id",
        "--isPublic", "True",
        "--workspaceUrl", "s3://some.workspace.url",
        "--jobEnv", '{"key":"val"}',
        "--machineType", "K80",
        "--name", "some_name",
        "--nodeAttrs", '{"key":"val"}',
        "--ports", "8080,9000:9900",
        "--projectId", "some_project_id",
        "--registryPassword", "some_registry_password",
        "--registryUsername", "some_registry_username",
        "--relDockerfilePath", "some dockerfile path",
        "--startedByUserId", "some_user_id",
        "--useDockerfile", "True",
        "--workingDirectory", "/some/path",
        "--workspaceUrl", "s3://some.workspace.url",
    ]
    BASIC_OPTIONS_REQUEST = {
        "name": u"exp1",
        "projectId": u"testHandle",
        "container": u"testContainer",
        "machineType": u"testType",
        "command": u"testCommand",
        "workspace": u"https://github.com/Paperspace/gradient-cli.git",
        "workspaceFileName": u"https://github.com/Paperspace/gradient-cli.git",
    }
    FULL_OPTIONS_REQUEST = {
        "clusterId": "some_cluster_id",
        "experimentId": "some_experiment_id",
        "cluster": "some_cluster_name",
        "startedByUserId": "some_user_id",
        "isPreemptible": True,
        "ignoreFiles": "file1,file2",
        "container": "some_container",
        "workingDirectory": "/some/path",
        "projectId": "some_project_id",
        "registryUsername": "some_registry_username",
        "workspaceUrl": "s3://some.workspace.url",
        "machineType": "K80",
        "registryPassword": "some_registry_password",
        "isPublic": True,
        "workspaceFileName": "s3://some.workspace.url",
        "jobEnv": {"key": "val"},
        "useDockerfile": True,
        "name": "some_name",
        "relDockerfilePath": "some dockerfile path",
        "targetNodeAttrs": {"key": "val"},
        "command": "some command",
        "ports": "8080,9000:9900",
    }
    RESPONSE_JSON_200 = {"id": "sadkfhlskdjh", "message": "success"}
    RESPONSE_CONTENT_200 = b'{"handle":"sadkfhlskdjh","message":"success"}\n'
    EXPECTED_STDOUT = u'New job created with ID: sadkfhlskdjh\n'

    RESPONSE_JSON_404_PROJECT_NOT_FOUND = {"details": {"handle": "wrong_handle"}, "error": "Project not found"}
    RESPONSE_CONTENT_404_PROJECT_NOT_FOUND = b'{"details":{"handle":"wrong_handle"},"error":"Project not found"}\n'
    EXPECTED_STDOUT_PROJECT_NOT_FOUND = "Project not found\nhandle: wrong_handle\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_job_was_run_with_basic_options(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, self.RESPONSE_CONTENT_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL + '/jobs/createJob/',
                                             headers=self.EXPECTED_HEADERS,
                                             json=None,
                                             params=self.BASIC_OPTIONS_REQUEST,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_job_was_run_with_all_options(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, self.RESPONSE_CONTENT_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.FULL_OPTIONS_COMMAND)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL + '/jobs/createJob/',
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=None,
                                             params=self.FULL_OPTIONS_REQUEST,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, post_patched, jobs_create_config_path):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, self.RESPONSE_CONTENT_200)
        command = ["jobs", "create", "--optionsFile", jobs_create_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL + '/jobs/createJob/',
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=None,
                                             params=self.FULL_OPTIONS_REQUEST,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0
