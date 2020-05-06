import json
import os
import shutil
import tempfile

import mock
import pytest
from click.testing import CliRunner

from gradient.api_sdk import sdk_exceptions
from gradient.api_sdk.clients.http_client import default_headers
from gradient.cli import cli
from tests import example_responses, MockResponse
from tests.example_responses import LIST_JOB_FILES_RESPONSE_JSON

EXPECTED_HEADERS = default_headers.copy()
EXPECTED_HEADERS["ps_client_name"] = "gradient-cli"

EXPECTED_HEADERS_WITH_CHANGED_API_KEY = EXPECTED_HEADERS.copy()
EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"


@pytest.fixture
def basic_options_metrics_stream_websocket_connection_iterator():
    def generator(self):
        yield """{"handle": "jstkd2lapucirs", "object_type": "mljob", "chart_name": "memoryUsage",
               "pod_metrics": {"mljob-ecgrgm7ok8chv-0-worker": {"time_stamp": 1588155670, "value": "5881856"}}}"""

        yield """{"handle": "jstkd2lapucirs", "object_type": "mljob", "chart_name": "cpuPercentage",
               "pod_metrics": {"mljob-ecgrgm7ok8chv-0-worker": {"time_stamp": 1588155670, "value": "0"}}}"""

        yield """{"handle": "jstkd2lapucirs", "object_type": "mljob", "chart_name": "memoryUsage",
               "pod_metrics": {"mljob-ecgrgm7ok8chv-0-worker": {"time_stamp": 1588155700, "value": "5881857"}}}"""

        raise sdk_exceptions.GradientSdkError()

    return generator


@pytest.fixture
def all_options_metrics_stream_websocket_connection_iterator():
    def generator(self):
        yield """{"handle": "jstkd2lapucirs", "object_type": "mljob", "chart_name": "gpuMemoryUsed",
               "pod_metrics": {"mljob-ecgrgm7ok8chv-0-worker": {"time_stamp": 1588155670, "value": "5881856"}}}"""

        yield """{"handle": "jstkd2lapucirs", "object_type": "mljob", "chart_name": "gpuMemoryFree",
               "pod_metrics": {"mljob-ecgrgm7ok8chv-0-worker": {"time_stamp": 1588155670, "value": "0"}}}"""

        yield """{"handle": "jstkd2lapucirs", "object_type": "mljob", "chart_name": "gpuMemoryUsed",
               "pod_metrics": {"mljob-ecgrgm7ok8chv-0-worker": {"time_stamp": 1588155700, "value": "5881857"}}}"""

        raise sdk_exceptions.GradientSdkError()

    return generator


class TestJobs(object):
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to fetch data: Invalid API token\n"
    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}

    EXPECTED_HEADERS = default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"


class TestListJobs(TestJobs):
    URL = "https://api.paperspace.io/jobs/getJobList/"
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
        "--tag", "some_tag",
        "--tag", "some_other_tag",
    ]
    EXPECTED_PARAMS_WITHOUT_FILTERING = {
        "filter": "{\"filter\": {\"where\": {}}}",
    }
    EXPECTED_REQUEST_PARAMS_WITH_FILTERING = {
        "filter": "{\"filter\": {\"where\": {\"projectId\": \"some_project_id\"}}}",
        "modelName": "team",
        "tagFilter[0]": "some_tag",
        "tagFilter[1]": "some_other_tag",
    }

    BASIC_COMMAND_WITH_MUTUALLY_EXCLUSIVE_FILTERS = [
        "jobs", "list",
        "--project", "some_project_name",
        "--projectId", "some_project_id",
    ]

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_and_print_table_when_jobs_list_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.EXPECTED_PARAMS_WITHOUT_FILTERING)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_jobs_list_was_used_with_api_key_option(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.EXPECTED_PARAMS_WITHOUT_FILTERING)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, get_patched, jobs_list_config_path):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [jobs_list_config_path]

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, command)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.EXPECTED_REQUEST_PARAMS_WITH_FILTERING)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_jobs_list_was_used_with_wrong_api_key(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.EXPECTED_PARAMS_WITHOUT_FILTERING)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_error_message_when_no_job_was_not_found(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_NO_JOBS_WERE_FOUND)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.EXPECTED_PARAMS_WITHOUT_FILTERING)
        assert result.output == self.EXPECTED_STDOUT_WHEN_NO_JOBS_WERE_FOUND
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.EXPECTED_PARAMS_WITHOUT_FILTERING)
        assert result.output == "Failed to fetch data\n"
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_jobs_list_was_used_with_filter_options(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_FILTERING)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.EXPECTED_REQUEST_PARAMS_WITH_FILTERING)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0


class TestJobLogs(TestJobs):
    URL = "https://logs.paperspace.io/jobs/logs"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_RESPONSE_JSON = example_responses.LIST_OF_LOGS_FOR_JOB
    COMMAND_WITHOUT_REQUIRED_PARAMETERS = ["jobs", "logs"]
    COMMAND_WITH_ALL_OPTIONS = [
        "jobs", "logs",
        "--id", "some_id",
        "--apiKey", "some_key",
        "--line", "50",
        "--limit", "200",
        # "--follow", "True",
    ]

    COMMAND_WITH_OPTIONS_FILE = ["jobs", "logs", "--optionsFile", ]  # path added in test
    REQUEST_WITH_OPTIONS_FILE = {"jobId": "some_id", "line": 50, "limit": 200}

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
    def test_should_send_valid_get_request_and_print_available_logs(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITH_ALL_OPTIONS)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_WITH_OPTIONS_FILE)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_get_request_when_log_list_was_used_with_wrong_api_key(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITH_ALL_OPTIONS)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
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
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
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
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
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
        result = self.runner.invoke(cli.cli, ["jobs", "artifacts", "destroy", "--id", job_id, "--files", file_names,
                                              "--apiKey", "some_key"])

        assert result.exit_code == 0, result.exc_info
        post_patched.assert_called_with("{}/jobs/{}/artifactsDestroy".format(self.URL, job_id),
                                        files=None,
                                        headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params={"files": file_names},
                                        data=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_post_request_when_destroying_artifacts_without_files_specified(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)
        job_id = "some_job_id"
        result = self.runner.invoke(cli.cli, ["jobs", "artifacts", "destroy", "--id", job_id, "--apiKey", "some_key"])

        post_patched.assert_called_with("{}/jobs/{}/artifactsDestroy".format(self.URL, job_id),
                                        files=None,
                                        headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
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
        post_patched.assert_called_with("{}/jobs/some_id/artifactsDestroy".format(self.URL),
                                        files=None,
                                        headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
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
        result = self.runner.invoke(cli.cli, ["jobs", "artifacts", "get", "--id", job_id, "--apiKey", "some_key"])

        get_patched.assert_called_with("{}/jobs/artifactsGet".format(self.URL),
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params={"jobId": job_id})
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, get_patched, jobs_artifacts_get_config_path):
        get_patched.return_value = MockResponse()
        command = ["jobs", "artifacts", "get", "--optionsFile", jobs_artifacts_get_config_path]

        result = self.runner.invoke(cli.cli, command)

        get_patched.assert_called_with("{}/jobs/artifactsGet".format(self.URL),
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
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
                                    ["jobs", "artifacts", "list", "--id", job_id, "--apiKey", "some_key", "--size",
                                     "--links",
                                     "--files", "foo"])

        get_patched.assert_called_with("{}/jobs/artifactsList".format(self.URL),
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
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
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
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
                                    ["jobs", "artifacts", "list", "--id", job_id, "--apiKey", "some_key"] + [option])

        get_patched.assert_called_with("{}/jobs/artifactsList".format(self.URL),
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params={"jobId": job_id,
                                               param: True})
        assert result.exit_code == 0


class TestJobsCreate(object):
    URL = "https://api.paperspace.io"
    TAGS_URL = "https://api.paperspace.io/entityTags/updateTags"
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
    BASIC_OPTIONS_COMMAND_WITH_TAGS = [
        "jobs", "create",
        "--name", "exp1",
        "--projectId", "testHandle",
        "--container", "testContainer",
        "--machineType", "testType",
        "--command", "testCommand",
        "--workspace", "https://github.com/Paperspace/gradient-cli.git",
        "--tag", "test0",
        "--tag", "test1",
        "--tags", "test2,test3",
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
        "--jobEnv", '{"key":"val"}',
        "--machineType", "K80",
        "--name", "some_name",
        "--nodeAttrs", '{"key":"val"}',
        "--ports", "8080,9000:9900",
        "--projectId", "some_project_id",
        "--registryPassword", "some_registry_password",
        "--registryUsername", "some_registry_username",
        "--registryTarget", "some_registry_target",
        "--registryTargetPassword", "some_registry_target_password",
        "--registryTargetUsername", "some_registry_target_username",
        "--relDockerfilePath", "some dockerfile path",
        "--startedByUserId", "some_user_id",
        "--useDockerfile", "True",
        "--workingDirectory", "/some/path",
        "--buildOnly",
        "--workspace", "s3://some-path",
    ]
    BASIC_OPTIONS_REQUEST = {
        "name": u"exp1",
        "projectId": u"testHandle",
        "container": u"testContainer",
        "machineType": u"testType",
        "command": u"testCommand",
        "workspaceFileName": u"https://github.com/Paperspace/gradient-cli.git",
    }
    FULL_OPTIONS_REQUEST = {
        "clusterId": "some_cluster_id",
        "experimentId": "some_experiment_id",
        "cluster": "some_cluster_name",
        "startedByUserId": "some_user_id",
        "isPreemptible": True,
        "container": "some_container",
        "workingDirectory": "/some/path",
        "projectId": "some_project_id",
        "registryTargetUsername": "some_registry_target_username",
        "machineType": "K80",
        "registryTargetPassword": "some_registry_target_password",
        "registryTarget": "some_registry_target",
        "isPublic": True,
        "workspaceFileName": "s3://some-path",
        "jobEnv": {"key": "val"},
        "useDockerfile": True,
        "name": "some_name",
        "relDockerfilePath": "some dockerfile path",
        "targetNodeAttrs": {"key": "val"},
        "command": "some command",
        "ports": "8080,9000:9900",
        "buildOnly": True,
        "registryUsername": "some_registry_username",
        "registryPassword": "some_registry_password",
    }
    TAGS_JSON = {
        "entity": "job",
        "entityId": "sadkfhlskdjh",
        "tags": ["test0", "test1", "test2", "test3"]
    }
    RESPONSE_JSON_200 = {"id": "sadkfhlskdjh", "message": "success"}
    UPDATE_TAGS_RESPONSE_JSON_200 = example_responses.UPDATE_TAGS_RESPONSE
    RESPONSE_CONTENT_200 = b'{"handle":"sadkfhlskdjh","message":"success"}\n'
    EXPECTED_STDOUT = u'New job created with ID: sadkfhlskdjh\n'
    EXPECTED_STDOUT_TAGS = u'New job created with ID: sadkfhlskdjh\n' \
                           u'https://www.paperspace.com/console/jobs/sadkfhlskdjh\n'

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
                                             headers=EXPECTED_HEADERS,
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
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
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
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=None,
                                             params=self.FULL_OPTIONS_REQUEST,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_tag_job(self, post_patched, get_patched, put_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, self.RESPONSE_CONTENT_200)
        get_patched.return_value = MockResponse({}, 200, "fake content")
        put_patched.return_value = MockResponse(self.UPDATE_TAGS_RESPONSE_JSON_200, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND_WITH_TAGS)

        post_patched.assert_called_once_with(self.URL + '/jobs/createJob/',
                                             headers=EXPECTED_HEADERS,
                                             json=None,
                                             params=self.BASIC_OPTIONS_REQUEST,
                                             files=None,
                                             data=None)

        put_patched.assert_called_once_with(
            self.TAGS_URL,
            headers=EXPECTED_HEADERS,
            json=self.TAGS_JSON,
            params=None,
            data=None,
        )

        assert result.output == self.EXPECTED_STDOUT_TAGS, result.exc_info
        assert result.exit_code == 0


class TestDownloadJobArtifacts(TestJobs):
    runner = CliRunner()
    LIST_FILES_URL = "https://api.paperspace.io/jobs/artifactsList"
    DESTINATION_DIR_NAME = "dest"
    DESTINATION_DIR_PATH = os.path.join(tempfile.gettempdir(), "dest")

    COMMAND = ["jobs", "artifacts", "download", "--id", "some_job_id", "--destinationDir", DESTINATION_DIR_PATH]

    @classmethod
    def teardown_method(cls):
        shutil.rmtree(cls.DESTINATION_DIR_PATH)

    @mock.patch("gradient.api_sdk.s3_downloader.requests.get")
    def test_should_get_a_list_of_files_and_download_them_to_defined_directory_when_download_command_was_executed(
            self, get_patched,
    ):
        file_response_mock = mock.MagicMock()
        file_response_mock.content = "\"Hello Paperspace!\n\""
        file_response_mock_2 = mock.MagicMock()
        file_response_mock_2.content = "\"Hello Paperspace 2\n\""
        file_response_mock_3 = mock.MagicMock()
        file_response_mock_3.content = "\"Elo\n\""
        get_patched.side_effect = [
            MockResponse(LIST_JOB_FILES_RESPONSE_JSON),
            file_response_mock,
            file_response_mock_2,
            file_response_mock_3,
        ]

        result = self.runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_has_calls([
            mock.call(self.LIST_FILES_URL,
                      headers=EXPECTED_HEADERS,
                      json=None,
                      params={"links": True, "jobId": "some_job_id"}),
            mock.call("https://ps-projects.s3.amazonaws.com/some/path/artifacts/hello.txt?AWSAccessKeyId="
                      "some_aws_access_key_id&Expires=713274132&Signature=7CT5k6buEmZe5k5E7g6BXMs2xV4%3D&"
                      "response-content-disposition=attachment%3Bfilename%3D%22hello.txt%22&x-amz-security-token="
                      "some_amz_security_token"),
            mock.call("https://ps-projects.s3.amazonaws.com/some/path/artifacts/hello2.txt?AWSAccessKeyId="
                      "some_aws_access_key_id&Expires=713274132&Signature=L1lI47cNyiROzdYkf%2FF3Cm3165E%3D&"
                      "response-content-disposition=attachment%3Bfilename%3D%22hello2.txt%22&x-amz-security-token="
                      "some_amz_security_token"),
            mock.call("https://ps-projects.s3.amazonaws.com/some/path/artifacts/keton/elo.txt?AWSAccessKeyId="
                      "some_aws_access_key_id&Expires=713274132&Signature=tHriojGx03S%2FKkVGQGVI5CQRFTo%3D&"
                      "response-content-disposition=attachment%3Bfilename%3D%22elo.txt%22&x-amz-security-token="
                      "some_amz_security_token"),
        ])
        assert os.path.exists(self.DESTINATION_DIR_PATH)
        assert os.path.isdir(self.DESTINATION_DIR_PATH)
        assert os.path.exists(os.path.join(self.DESTINATION_DIR_PATH, "keton"))
        assert os.path.isdir(os.path.join(self.DESTINATION_DIR_PATH, "keton"))

        hello_txt_path = os.path.join(self.DESTINATION_DIR_PATH, "hello.txt")
        assert os.path.exists(hello_txt_path)
        assert not os.path.isdir(hello_txt_path)
        with open(hello_txt_path) as h:
            assert h.read() == "\"Hello Paperspace!\n\""

        hello2_txt_path = os.path.join(self.DESTINATION_DIR_PATH, "hello2.txt")
        assert os.path.exists(hello2_txt_path)
        assert not os.path.isdir(hello2_txt_path)
        with open(hello2_txt_path) as h:
            assert h.read() == "\"Hello Paperspace 2\n\""

        elo_txt_path = os.path.join(self.DESTINATION_DIR_PATH, "keton", "elo.txt")
        assert os.path.exists(elo_txt_path)
        assert not os.path.isdir(elo_txt_path)
        with open(elo_txt_path) as h:
            assert h.read() == "\"Elo\n\""

        assert result.exit_code == 0


class TestJobsMetricsGetCommand(object):
    GET_JOB_URL = "https://api.paperspace.io/jobs/getPublicJob"
    GET_METRICS_URL = "https://aws-testing.paperspace.io/metrics/api/v1/range"
    BASIC_OPTIONS_COMMAND = [
        "jobs", "metrics", "get",
        "--id", "jstkd2lapucirs",
    ]
    ALL_OPTIONS_COMMAND = [
        "jobs", "metrics", "get",
        "--id", "jstkd2lapucirs",
        "--metric", "gpuMemoryFree",
        "--metric", "gpuMemoryUsed",
        "--interval", "20s",
        "--start", "2020-04-01",
        "--end", "2020-04-02 21:37:00",
        "--apiKey", "some_key",
    ]
    FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE = [
        "jobs", "metrics", "get",
        "--optionsFile",  # path added in test,
    ]

    GET_JOB_REQUEST_JSON = {"jobId": "jstkd2lapucirs"}
    BASIC_COMMAND_GET_METRICS_REQUEST_PARAMS = {
        "start": "2020-04-29T10:11:07Z",
        "handle": "jstkd2lapucirs",
        "interval": "30s",
        "charts": "cpuPercentage,memoryUsage",
        "objecttype": "mljob",
    }
    ALL_COMMANDS_GET_METRICS_REQUEST_PARAMS = {
        "start": "2020-04-01T00:00:00Z",
        "handle": "jstkd2lapucirs",
        "interval": "20s",
        "charts": "gpuMemoryFree,gpuMemoryUsed",
        "objecttype": "mljob",
        "end": "2020-04-02T21:37:00Z",
    }

    GET_JOB_RESPONSE_JSON = example_responses.GET_JOB_RESPONSE
    GET_METRICS_RESPONSE_JSON = example_responses.GET_JOB_METRICS_RESPONSE
    GET_JOB_RESPONSE_JSON_WHEN_NO_JOBS_WERE_FOUND = {
        "error": {
            "name": "ApplicationError",
            "status": 404,
            "message": "No such job",
        },
    }

    EXPECTED_STDOUT = """{
  "cpuPercentage": {
    "mljob-ecgrgm7ok8chv-0-worker": [
      {
        "time_stamp": 1588155157, 
        "value": "0"
      }, 
      {
        "time_stamp": 1588155187, 
        "value": "0"
      }, 
      {
        "time_stamp": 1588155217, 
        "value": "0"
      }
    ]
  }, 
  "memoryUsage": {
    "mljob-ecgrgm7ok8chv-0-worker": [
      {
        "time_stamp": 1588155097, 
        "value": "0"
      }, 
      {
        "time_stamp": 1588155127, 
        "value": "5881856"
      }, 
      {
        "time_stamp": 1588155157, 
        "value": "5881856"
      }, 
      {
        "time_stamp": 1588155187, 
        "value": "5881856"
      }
    ]
  }
}
"""

    EXPECTED_STDOUT_WHEN_INVALID_API_KEY_WAS_USED = "Failed to fetch data: Invalid API token\n"
    EXPECTED_STDOUT_WHEN_EXPERIMENT_WAS_NOT_FOUND = "Failed to fetch data: No such job\n"
    EXPECTED_STDOUT_WHEN_NO_METRICS_FOUND = """{
    "cpuPercentage": null,
    "memoryUsage": null
}
"""
    EXPECTED_STDOUT_WHEN_ERROR_CODE_WAS_RETURNED_WITHOUT_ERROR_MESSAGE = "Failed to fetch data\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_all_available_metrics_when_metrics_get_command_was_used_with_basic_options(
            self, post_patched, get_patched):
        post_patched.return_value = MockResponse(self.GET_JOB_RESPONSE_JSON)
        get_patched.return_value = MockResponse(self.GET_METRICS_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        assert json.loads(result.output.strip()) == json.loads(self.EXPECTED_STDOUT.strip()), \
            str(result.output) + str(result.exc_info)
        post_patched.assert_called_once_with(
            self.GET_JOB_URL,
            json=self.GET_JOB_REQUEST_JSON,
            params=None,
            data=None,
            files=None,
            headers=EXPECTED_HEADERS,
        )
        get_patched.assert_called_once_with(
            self.GET_METRICS_URL,
            json=None,
            params=self.BASIC_COMMAND_GET_METRICS_REQUEST_PARAMS,
            headers=EXPECTED_HEADERS,
        )
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_metrics_when_metrics_get_command_was_used_with_all_options(
            self, post_patched, get_patched):
        post_patched.return_value = MockResponse(self.GET_JOB_RESPONSE_JSON)
        get_patched.return_value = MockResponse(self.GET_METRICS_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        # comparing objects instead of strings because Py2 and Py3 produce slightly different outputs
        assert json.loads(result.output.strip()) == json.loads(self.EXPECTED_STDOUT.strip()), result.exc_info
        post_patched.assert_called_once_with(
            self.GET_JOB_URL,
            json=self.GET_JOB_REQUEST_JSON,
            params=None,
            data=None,
            files=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )
        get_patched.assert_called_once_with(
            self.GET_METRICS_URL,
            json=None,
            params=self.ALL_COMMANDS_GET_METRICS_REQUEST_PARAMS,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_metrics_when_metrics_get_was_executed_and_options_file_was_used(
            self, post_patched, get_patched, jobs_metrics_get_config_path):
        post_patched.return_value = MockResponse(self.GET_JOB_RESPONSE_JSON)
        get_patched.return_value = MockResponse(self.GET_METRICS_RESPONSE_JSON)

        command = self.FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE[:] + [jobs_metrics_get_config_path]
        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        # comparing objects instead of strings because Py2 and Py3 produce slightly different outputs
        assert json.loads(result.output.strip()) == json.loads(self.EXPECTED_STDOUT.strip()), result.exc_info
        post_patched.assert_called_once_with(
            self.GET_JOB_URL,
            json=self.GET_JOB_REQUEST_JSON,
            params=None,
            data=None,
            files=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )
        get_patched.assert_called_once_with(
            self.GET_METRICS_URL,
            json=None,
            params=self.ALL_COMMANDS_GET_METRICS_REQUEST_PARAMS,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_invalid_api_key_was_used(self, post_patched):
        post_patched.return_value = MockResponse({"status": 400, "message": "Invalid API token"}, status_code=400)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_INVALID_API_KEY_WAS_USED, result.exc_info

        post_patched.assert_called_once_with(
            self.GET_JOB_URL,
            json=self.GET_JOB_REQUEST_JSON,
            params=None,
            data=None,
            files=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_job_was_not_found(self, post_patched):
        post_patched.return_value = MockResponse(self.GET_JOB_RESPONSE_JSON_WHEN_NO_JOBS_WERE_FOUND, status_code=400)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_EXPERIMENT_WAS_NOT_FOUND, result.exc_info

        post_patched.assert_called_once_with(
            self.GET_JOB_URL,
            json=self.GET_JOB_REQUEST_JSON,
            params=None,
            data=None,
            files=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_message_when_was_no_metrics_were_returned(
            self, post_patched, get_patched):
        post_patched.return_value = MockResponse(self.GET_JOB_RESPONSE_JSON)
        get_patched.return_value = MockResponse(example_responses.JOBS_METRICS_GET_RESPONSE_WHEN_NO_DATA_WAS_FOUND)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert json.loads(result.output.strip()) == json.loads(self.EXPECTED_STDOUT_WHEN_NO_METRICS_FOUND.strip()), \
            result.exc_info

        post_patched.assert_called_once_with(
            self.GET_JOB_URL,
            json=self.GET_JOB_REQUEST_JSON,
            params=None,
            data=None,
            files=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )
        get_patched.assert_called_once_with(
            self.GET_METRICS_URL,
            json=None,
            params=self.ALL_COMMANDS_GET_METRICS_REQUEST_PARAMS,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_error_code_was_returned_without_error_message(
            self, post_patched, get_patched):
        post_patched.return_value = MockResponse(self.GET_JOB_RESPONSE_JSON)
        get_patched.return_value = MockResponse(status_code=500)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_ERROR_CODE_WAS_RETURNED_WITHOUT_ERROR_MESSAGE, result.exc_info
        post_patched.assert_called_once_with(
            self.GET_JOB_URL,
            json=self.GET_JOB_REQUEST_JSON,
            params=None,
            data=None,
            files=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )
        get_patched.assert_called_once_with(
            self.GET_METRICS_URL,
            json=None,
            params=self.ALL_COMMANDS_GET_METRICS_REQUEST_PARAMS,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        assert result.exit_code == 0, result.exc_info


class TestExperimentsMetricsStreamCommand(object):
    GET_JOB_URL = "https://api.paperspace.io/jobs/getPublicJob"
    GET_METRICS_URL = "https://aws-testing.paperspace.io/metrics/api/v1/stream"
    BASIC_OPTIONS_COMMAND = [
        "jobs", "metrics", "stream",
        "--id", "jstkd2lapucirs",
    ]
    ALL_OPTIONS_COMMAND = [
        "jobs", "metrics", "stream",
        "--id", "jstkd2lapucirs",
        "--metric", "gpuMemoryFree",
        "--metric", "gpuMemoryUsed",
        "--interval", "20s",
        "--apiKey", "some_key",
    ]
    ALL_OPTIONS_COMMAND_WITH_OPTIONS_FILE = [
        "jobs", "metrics", "stream",
        "--optionsFile",  # path added in test,
    ]

    GET_JOB_REQUEST_JSON = {"jobId": "jstkd2lapucirs"}
    BASIC_COMMAND_CHART_DESCRIPTOR = '{"chart_names": ["cpuPercentage", "memoryUsage"], "handles": ["jstkd2lapucirs"]' \
                                     ', "object_type": "mljob", "poll_interval": "30s"}'
    ALL_COMMANDS_CHART_DESCRIPTOR = '{"chart_names": ["gpuMemoryFree", "gpuMemoryUsed"], "handles": ["jstkd2lapucirs"' \
                                    '], "object_type": "mljob", "poll_interval": "20s"}'

    GET_JOB_RESPONSE_JSON = example_responses.GET_JOB_RESPONSE

    EXPECTED_TABLE_1 = """+------------------------------+---------------+-------------+
| Pod                          | cpuPercentage | memoryUsage |
+------------------------------+---------------+-------------+
| mljob-ecgrgm7ok8chv-0-worker |               | 5881856     |
+------------------------------+---------------+-------------+
"""
    EXPECTED_TABLE_2 = """+------------------------------+---------------+-------------+
| Pod                          | cpuPercentage | memoryUsage |
+------------------------------+---------------+-------------+
| mljob-ecgrgm7ok8chv-0-worker | 0             | 5881856     |
+------------------------------+---------------+-------------+
"""
    EXPECTED_TABLE_3 = """+------------------------------+---------------+-------------+
| Pod                          | cpuPercentage | memoryUsage |
+------------------------------+---------------+-------------+
| mljob-ecgrgm7ok8chv-0-worker | 0             | 5881857     |
+------------------------------+---------------+-------------+
"""

    ALL_OPTIONS_EXPECTED_TABLE_1 = """+------------------------------+---------------+---------------+
| Pod                          | gpuMemoryFree | gpuMemoryUsed |
+------------------------------+---------------+---------------+
| mljob-ecgrgm7ok8chv-0-worker |               | 5881856       |
+------------------------------+---------------+---------------+
"""
    ALL_OPTIONS_EXPECTED_TABLE_2 = """+------------------------------+---------------+---------------+
| Pod                          | gpuMemoryFree | gpuMemoryUsed |
+------------------------------+---------------+---------------+
| mljob-ecgrgm7ok8chv-0-worker | 0             | 5881856       |
+------------------------------+---------------+---------------+
"""
    ALL_OPTIONS_EXPECTED_TABLE_3 = """+------------------------------+---------------+---------------+
| Pod                          | gpuMemoryFree | gpuMemoryUsed |
+------------------------------+---------------+---------------+
| mljob-ecgrgm7ok8chv-0-worker | 0             | 5881857       |
+------------------------------+---------------+---------------+
"""

    EXPECTED_STDOUT_WHEN_INVALID_API_KEY_WAS_USED = "Failed to fetch data: Incorrect API Key provided\nForbidden\n"
    EXPECTED_STDOUT_WHEN_JOB_WAS_NOT_FOUND = "Failed to fetch data: No such job\n"

    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_all_available_metrics_when_metrics_get_command_was_used_with_basic_options(
            self, post_patched, create_ws_connection_patched,
            basic_options_metrics_stream_websocket_connection_iterator):
        post_patched.return_value = MockResponse(self.GET_JOB_RESPONSE_JSON)

        ws_connection_instance_mock = mock.MagicMock()
        ws_connection_instance_mock.__iter__ = basic_options_metrics_stream_websocket_connection_iterator
        create_ws_connection_patched.return_value = ws_connection_instance_mock

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        assert self.EXPECTED_TABLE_1 in result.output, result.exc_info
        assert self.EXPECTED_TABLE_2 in result.output, result.exc_info
        assert self.EXPECTED_TABLE_3 in result.output, result.exc_info

        post_patched.assert_called_once_with(
            self.GET_JOB_URL,
            json=self.GET_JOB_REQUEST_JSON,
            params=None,
            data=None,
            files=None,
            headers=EXPECTED_HEADERS,
        )
        ws_connection_instance_mock.send.assert_called_once_with(self.BASIC_COMMAND_CHART_DESCRIPTOR)
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_metrics_when_metrics_get_command_was_used_with_all_options(
            self, post_patched, create_ws_connection_patched,
            all_options_metrics_stream_websocket_connection_iterator):
        post_patched.return_value = MockResponse(self.GET_JOB_RESPONSE_JSON)

        ws_connection_instance_mock = mock.MagicMock()
        ws_connection_instance_mock.__iter__ = all_options_metrics_stream_websocket_connection_iterator
        create_ws_connection_patched.return_value = ws_connection_instance_mock

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert self.ALL_OPTIONS_EXPECTED_TABLE_1 in result.output, result.exc_info
        assert self.ALL_OPTIONS_EXPECTED_TABLE_2 in result.output, result.exc_info
        assert self.ALL_OPTIONS_EXPECTED_TABLE_3 in result.output, result.exc_info

        post_patched.assert_called_once_with(
            self.GET_JOB_URL,
            json=self.GET_JOB_REQUEST_JSON,
            params=None,
            data=None,
            files=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        ws_connection_instance_mock.send.assert_called_once_with(self.ALL_COMMANDS_CHART_DESCRIPTOR)
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_metrics_when_metrics_get_was_executed_and_options_file_was_used(
            self, post_patched, create_ws_connection_patched,
            all_options_metrics_stream_websocket_connection_iterator,
            jobs_metrics_stream_config_path):
        post_patched.return_value = MockResponse(self.GET_JOB_RESPONSE_JSON)
        ws_connection_instance_mock = mock.MagicMock()
        ws_connection_instance_mock.__iter__ = all_options_metrics_stream_websocket_connection_iterator
        create_ws_connection_patched.return_value = ws_connection_instance_mock

        command = self.ALL_OPTIONS_COMMAND_WITH_OPTIONS_FILE[:] + [jobs_metrics_stream_config_path]
        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.ALL_OPTIONS_EXPECTED_TABLE_1 in result.output, result.exc_info
        assert self.ALL_OPTIONS_EXPECTED_TABLE_2 in result.output, result.exc_info
        assert self.ALL_OPTIONS_EXPECTED_TABLE_3 in result.output, result.exc_info

        post_patched.assert_called_once_with(
            self.GET_JOB_URL,
            json=self.GET_JOB_REQUEST_JSON,
            params=None,
            data=None,
            files=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        ws_connection_instance_mock.send.assert_called_once_with(self.ALL_COMMANDS_CHART_DESCRIPTOR)
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_invalid_api_key_was_used(
            self, post_patched, create_ws_connection_patched):
        post_patched.return_value = MockResponse({"status": 400, "message": "Invalid API token"}, 400)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert "Failed to fetch data: Invalid API token\n" == result.output, result.exc_info

        post_patched.assert_called_once_with(
            self.GET_JOB_URL,
            json=self.GET_JOB_REQUEST_JSON,
            params=None,
            data=None,
            files=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        create_ws_connection_patched.assert_not_called()
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_job_was_not_found(
            self, post_patched, create_ws_connection_patched):
        post_patched.return_value = MockResponse(
            {"error": {"name": "ApplicationError", "status": 404, "message": "No such job"}},
            404,
        )

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_JOB_WAS_NOT_FOUND, result.exc_info

        post_patched.assert_called_once_with(
            self.GET_JOB_URL,
            json=self.GET_JOB_REQUEST_JSON,
            params=None,
            data=None,
            files=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        create_ws_connection_patched.assert_not_called()
        assert result.exit_code == 0, result.exc_info
