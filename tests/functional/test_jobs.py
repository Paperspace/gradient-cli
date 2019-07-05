import mock
import pytest
from click.testing import CliRunner

from gradient.cli import cli
from gradient.client import default_headers
from tests import example_responses, MockResponse


class TestJobs(object):
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Invalid API token\n"
    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}

    EXPECTED_HEADERS = default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"


class TestListJobs(TestJobs):
    URL = "https://api.paperspace.io/jobs/getJobs/"
    BASIC_COMMAND = ["jobs", "list"]
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
        "--project", "some_project_name",
        "--experimentId", "some_experiment_id",
    ]
    EXPECTED_REQUEST_JSON_WITH_FILTERING = {
        "project": "some_project_name",
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
    EXPECTED_STDOUT_WHEN_MUTUALLY_EXCLUSIVE_FILTERS = "Incompatible parameters: project and projectId " \
                                                      "cannot both be specified\n"

    @mock.patch("gradient.client.requests.get")
    def test_should_send_valid_post_request_and_print_table_when_jobs_list_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.client.requests.get")
    def test_should_send_valid_post_request_when_jobs_list_was_used_with_api_key_option(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.client.requests.get")
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

    @mock.patch("gradient.client.requests.get")
    def test_should_print_error_message_when_no_job_was_not_found(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_NO_JOBS_WERE_FOUND,
                                                status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT_WHEN_NO_JOBS_WERE_FOUND
        assert result.exit_code == 0

    @mock.patch("gradient.client.requests.get")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=None)
        assert result.output == "Error while parsing response data: No JSON\n"
        assert result.exit_code == 0

    @mock.patch("gradient.client.requests.get")
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

    @mock.patch("gradient.client.requests.get")
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
    BASIC_COMMAND_WITHOUT_PARAMETERS = ["jobs", "logs"]
    BASIC_COMMAND = ["jobs", "logs", "--jobId", "some_job_id", "--apiKey", "some_key"]
    BASIC_COMMAND_PARAMS = {"jobId": "some_job_id", "line": 0, "limit": 10000}

    EXPECTED_STDOUT_WITHOUT_PARAMETERS = """Usage: cli jobs logs [OPTIONS]
Try "cli jobs logs --help" for help.

Error: Missing option "--jobId".
"""

    EXPECTED_STDOUT = """+Job some_job_id logs--------------------------------------------------------------------+
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
| 10   | AttributeError: module 'tensorflow' has no attribute 'Dimension'                |
| 11   | PSEOF                                                                           |
+------+---------------------------------------------------------------------------------+
"""

    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Invalid API token\n"

    @mock.patch("gradient.client.requests.get")
    def test_command_should_not_send_request_without_required_parameters(self, get_patched):
        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITHOUT_PARAMETERS)
        print(result)

        get_patched.assert_not_called()
        assert result.exit_code == 2
        assert result.output == self.EXPECTED_STDOUT_WITHOUT_PARAMETERS

    @mock.patch("gradient.client.requests.get")
    def test_should_send_valid_get_request_and_print_available_logs(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.BASIC_COMMAND_PARAMS)

        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.client.requests.get")
    def test_should_send_valid_get_request_when_log_list_was_used_with_wrong_api_key(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.BASIC_COMMAND_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("gradient.client.requests.get")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.BASIC_COMMAND_PARAMS)
        assert result.output == "Error while parsing response data: No JSON\n"
        assert result.exit_code == 0


class TestJobArtifactsCommands(TestJobs):
    runner = CliRunner()
    URL = "https://api.paperspace.io"

    @mock.patch("gradient.client.requests.post")
    def test_should_send_valid_post_request_when_destroying_artifacts_with_files_specified(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)
        job_id = "some_job_id"
        file_names = "some_file_names"
        result = self.runner.invoke(cli.cli, ["jobs", "artifacts", "destroy", job_id, "--files", file_names, "--apiKey",
                                              "some_key"])

        post_patched.assert_called_with("{}/jobs/{}/artifactsDestroy".format(self.URL, job_id),
                                        files=None,
                                        headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params={"files": file_names},
                                        data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.client.requests.post")
    def test_should_send_valid_post_request_when_destroying_artifacts_without_files_specified(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)
        job_id = "some_job_id"
        result = self.runner.invoke(cli.cli, ["jobs", "artifacts", "destroy", job_id, "--apiKey", "some_key"])

        post_patched.assert_called_with("{}/jobs/{}/artifactsDestroy".format(self.URL, job_id),
                                        files=None,
                                        headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params=None,
                                        data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.client.requests.get")
    def test_should_send_send_valid_get_request_and_receive_json_response(self, get_patched):
        get_patched.return_value = MockResponse(status_code=200)
        job_id = "some_job_id"
        result = self.runner.invoke(cli.cli, ["jobs", "artifacts", "get", job_id, "--apiKey", "some_key"])

        get_patched.assert_called_with("{}/jobs/artifactsGet".format(self.URL),
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params={"jobId": job_id})
        assert result.exit_code == 0

    @mock.patch("gradient.client.requests.get")
    def test_should_send_valid_get_request_with_all_parameters_for_a_list_of_artifacts(self, get_patched):
        get_patched.return_value = MockResponse(status_code=200)
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

    @mock.patch("gradient.client.requests.get")
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
        "--name", "exp1",
        "--ports", 4567,
        "--workspaceUrl", "wsp.url",
        "--workingDirectory", "/work/dir/",
        "--artifactDirectory", "/artifact/dir/",
        "--clusterId", 42,
        "--experimentEnv", '{"key":"val"}',
        "--projectId", "testHandle",
        "--container", "testContainer",
        "--machineType", "testType",
        "--command", "testCommand",
        "--containerUser", "conUser",
        "--registryUsername", "userName",
        "--registryPassword", "passwd",
        "--apiKey", "some_key",
    ]
    BASIC_OPTIONS_REQUEST = {
        "name": u"exp1",
        "projectId": u"testHandle",
        "container": u"testContainer",
        "machineType": u"testType",
        "command": u"testCommand",
        "workspaceUrl": u"https://github.com/Paperspace/gradient-cli.git",
        "workspaceFileName": u"https://github.com/Paperspace/gradient-cli.git",
    }
    FULL_OPTIONS_REQUEST = {
        "name": u"exp1",
        "ports": 4567,
        "workspaceUrl": u"wsp.url",
        "workingDirectory": u"/work/dir/",
        "artifactDirectory": u"/artifact/dir/",
        "clusterId": 42,
        "experimentEnv": {u"key": u"val"},
        "projectHandle": u"testHandle",
        "container": u"testContainer",
        "machineType": u"testType",
        "command": u"testCommand",
        "containerUser": u"conUser",
        "registryUsername": u"userName",
        "registryPassword": u"passwd",
    }
    RESPONSE_JSON_200 = {"id": "sadkfhlskdjh", "message": "success"}
    RESPONSE_CONTENT_200 = b'{"handle":"sadkfhlskdjh","message":"success"}\n'
    EXPECTED_STDOUT = u'Creating job...\nJob created - ID: sadkfhlskdjh\n'

    RESPONSE_JSON_404_PROJECT_NOT_FOUND = {"details": {"handle": "wrong_handle"}, "error": "Project not found"}
    RESPONSE_CONTENT_404_PROJECT_NOT_FOUND = b'{"details":{"handle":"wrong_handle"},"error":"Project not found"}\n'
    EXPECTED_STDOUT_PROJECT_NOT_FOUND = "Project not found\nhandle: wrong_handle\n"

    @mock.patch("gradient.client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_job_was_run_with_basic_options(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, self.RESPONSE_CONTENT_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        post_patched.assert_called_once_with(self.URL + '/jobs/createJob/',
                                             headers=self.EXPECTED_HEADERS,
                                             json=None,
                                             params=self.BASIC_OPTIONS_REQUEST,
                                             files=None,
                                             data=None)

        assert self.EXPECTED_STDOUT in result.output
        assert result.exit_code == 0
