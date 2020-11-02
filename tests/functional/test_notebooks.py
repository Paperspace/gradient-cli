import json

import mock
import pytest
from click.testing import CliRunner

from gradient.api_sdk import sdk_exceptions
from gradient.api_sdk.clients.http_client import default_headers
from gradient.cli import cli
from tests import MockResponse, example_responses

EXPECTED_HEADERS = default_headers.copy()
EXPECTED_HEADERS["ps_client_name"] = "gradient-cli"

EXPECTED_HEADERS_WITH_CHANGED_API_KEY = EXPECTED_HEADERS.copy()
EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"


@pytest.fixture
def basic_options_metrics_stream_websocket_connection_iterator():
    def generator(self):
        yield """{"handle":"nrwed38p","object_type":"notebook","chart_name":"memoryUsage",
        "pod_metrics":{"nrwed38p":{"time_stamp":1588066152,"value":"54013952"}}}"""
        yield """{"handle":"nrwed38p","object_type":"notebook","chart_name":"cpuPercentage",
        "pod_metrics":{"nrwed38p":{"time_stamp":1588066152,"value":"0.006907773333334353"}}}"""
        yield """{"handle":"nrwed38p","object_type":"notebook","chart_name":"memoryUsage",
        "pod_metrics":{"nrwed38p":{"time_stamp":1588066155,"value":"12345667"}}}"""

        raise sdk_exceptions.EndWebsocketStream()

    return generator


@pytest.fixture
def all_options_metrics_stream_websocket_connection_iterator():
    def generator(self):
        yield """{"handle":"nrwed38p","object_type":"notebook","chart_name":"gpuMemoryFree",
        "pod_metrics":{"nrwed38p":{"time_stamp":1588068626,"value":"1234"}}}"""
        yield """{"handle":"nrwed38p","object_type":"notebook","chart_name":"gpuMemoryUsed",
        "pod_metrics":{"nrwed38p":{"time_stamp":1588068646,"value":"32"}}}"""
        yield """{"handle":"nrwed38p","object_type":"notebook","chart_name":"gpuMemoryFree",
        "pod_metrics":{"nrwed38p":{"time_stamp":1588068646,"value":"2345"}}}"""

        raise sdk_exceptions.EndWebsocketStream()

    return generator


class TestNotebooksCreate(object):
    URL = "https://api.paperspace.io/notebooks/v2/createNotebook"
    COMMAND = [
        "notebooks",
        "create",
        "--machineType", "P5000",
        "--container", "jupyter/notebook",
        "--projectId", "pr1234",
        "--clusterId", "321",
    ]
    EXPECTED_REQUEST_JSON = {
        "machineType": "P5000",
        "container": "jupyter/notebook",
        "clusterId": "321",
        "isPreemptible": False,
        "isPublic": False,
        "workspace": "none",
        "projectId": "pr1234",
    }
    EXPECTED_RESPONSE_JSON = {
        "handle": "some_id",
        "notebookToken": None,
        "jobId": 20163,
        "isPublic": False,
        "id": 1811,
        "container": "jupyter/notebook",
    }
    EXPECTED_STDOUT = "Created new notebook with id: some_id\n" \
                      "https://console.paperspace.com/some_namespace/notebook/prg284tu2\n"

    COMMAND_WITH_API_KEY_USED = [
        "notebooks",
        "create",
        "--machineType", "P5000",
        "--container", "jupyter/notebook",
        "--projectId", "pr1234",
        "--clusterId", "321",
        "--apiKey", "some_key",
    ]

    COMMAND_WITH_ALL_OPTIONS = [
        "notebooks",
        "create",
        "--machineType", "P5000",
        "--container", "jupyter/notebook",
        "--projectId", "pr1234",
        "--clusterId", "321",
        "--name", "some_notebook_name",
        "--registryUsername", "some_username",
        "--registryPassword", "some_password",
        "--command", "some_entrypoint",
        "--containerUser", "some_container_user",
        "--shutdownTimeout", "8",
        "--environment", '{"key":"val"}',
        "--isPreemptible",
        "--workspace", "https://github.com/fake/repo.git",
    ]
    EXPECTED_REQUEST_JSON_WITH_ALL_OPTIONS = {
        "machineType": "P5000",
        "container": "jupyter/notebook",
        "projectId": "pr1234",
        "clusterId": "321",
        "name": "some_notebook_name",
        "registryUsername": "some_username",
        "registryPassword": "some_password",
        "command": "c29tZV9lbnRyeXBvaW50",
        "containerUser": "some_container_user",
        "environment": {"key": "val"},
        "shutdownTimeout": 8,
        "isPreemptible": True,
        "isPublic": False,
        "workspace": "https://github.com/fake/repo.git",
    }
    COMMAND_WITH_OPTIONS_FILE_USED = ["notebooks", "create", "--optionsFile", ]  # path added in test

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to create resource: Invalid API token\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_and_print_notebook_id(self, post_patched, get_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)
        get_patched.return_value = MockResponse(example_responses.NOTEBOOK_GET_RESPONSE)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             data=None,
                                             files=None,
                                             params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, post_patched, get_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)
        get_patched.return_value = MockResponse(example_responses.NOTEBOOK_GET_RESPONSE)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_USED)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             data=None,
                                             files=None,
                                             params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_and_print_notebook_id_when_all_options_were_used(self, post_patched, get_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)
        get_patched.return_value = MockResponse(example_responses.NOTEBOOK_GET_RESPONSE)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_ALL_OPTIONS)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON_WITH_ALL_OPTIONS,
                                             data=None,
                                             files=None,
                                             params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_option_from_yaml_file(self, post_patched, get_patched, notebooks_create_config_path):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)
        get_patched.return_value = MockResponse(example_responses.NOTEBOOK_GET_RESPONSE)
        command = self.COMMAND_WITH_OPTIONS_FILE_USED[:] + [notebooks_create_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON_WITH_ALL_OPTIONS,
                                             data=None,
                                             files=None,
                                             params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_command_was_used_with_invalid_api_token(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN, result.exc_info
        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=self.EXPECTED_REQUEST_JSON,
                                        data=None,
                                        files=None,
                                        params=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, post_patched):
        post_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == "Failed to create resource\n", result.exc_info
        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=self.EXPECTED_REQUEST_JSON,
                                        data=None,
                                        files=None,
                                        params=None)
        assert result.exit_code == 0


# TODO: Add test case for creating notebook with tag

class TestNotebooksFork(object):
    URL = "https://api.paperspace.io/notebooks/v2/forkNotebook"
    COMMAND = [
        "notebooks",
        "fork",
        "--id", "n1234",
        "--projectId", "p1234",
    ]
    EXPECTED_REQUEST_JSON = {
        "notebookId": "n1234",
        "projectId": "p1234",
    }
    EXPECTED_RESPONSE_JSON = {
        "handle": "n1234",
        "notebookToken": None,
        "jobId": 20163,
        "isPublic": False,
        "id": 1811,
    }
    EXPECTED_STDOUT = "Notebook forked to id: n1234\n"

    COMMAND_WITH_API_KEY_USED = [
        "notebooks",
        "fork",
        "--id", "n1234",
        "--projectId", "p1234",
        "--apiKey", "some_key",
    ]
    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to fork notebook: Invalid API token\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_and_print_notebook_id(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             data=None,
                                             files=None,
                                             params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_USED)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             data=None,
                                             files=None,
                                             params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_command_was_used_with_invalid_api_token(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN, result.exc_info
        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=self.EXPECTED_REQUEST_JSON,
                                        data=None,
                                        files=None,
                                        params=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, post_patched):
        post_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == "Failed to fork notebook\n", result.exc_info
        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=self.EXPECTED_REQUEST_JSON,
                                        data=None,
                                        files=None,
                                        params=None)
        assert result.exit_code == 0


class TestNotebooksStart(object):
    URL = "https://api.paperspace.io/notebooks/v2/startNotebook"
    COMMAND = [
        "notebooks",
        "start",
        "--id", "n123",
        "--machineType", "c5.xlarge",
        "--clusterId", "cl123",
    ]
    EXPECTED_REQUEST_JSON = {
        "notebookId": "n123",
        "machineType": "c5.xlarge",
        "clusterId": "cl123",
        "isPreemptible": False,
    }
    EXPECTED_RESPONSE_JSON = {
        "handle": "n123",
        "notebookToken": None,
        "jobId": 20163,
        "isPublic": False,
        "id": 1811,
        "containerId": 123,
    }
    EXPECTED_STDOUT = "Started notebook with id: n123\n"
    COMMAND_WITH_API_KEY_USED = [
        "notebooks",
        "start",
        "--id", "n123",
        "--machineType", "c5.xlarge",
        "--clusterId", "cl123",
        "--apiKey", "some_key",
    ]
    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to create resource: Invalid API token\n"
    EXPECTED_STDOUT_WITH_KEY = "Started notebook with id: n123\n" \
                               "https://console.paperspace.com/some_namespace/notebook/prg284tu2\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, post_patched, get_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)
        get_patched.return_value = MockResponse(example_responses.NOTEBOOK_GET_RESPONSE)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_USED)

        assert result.output == self.EXPECTED_STDOUT_WITH_KEY, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             data=None,
                                             files=None,
                                             params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_command_was_used_with_invalid_api_token(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN, result.exc_info
        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=self.EXPECTED_REQUEST_JSON,
                                        data=None,
                                        files=None,
                                        params=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, post_patched):
        post_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == "Failed to create resource\n", result.exc_info
        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=self.EXPECTED_REQUEST_JSON,
                                        data=None,
                                        files=None,
                                        params=None)
        assert result.exit_code == 0


class TestNotebooksStop(object):
    URL = "https://api.paperspace.io/notebooks/v2/stopNotebook"
    COMMAND = [
        "notebooks",
        "stop",
        "--id", "n123",
    ]
    EXPECTED_REQUEST_JSON = {
        "notebookId": 'n123',
    }
    EXPECTED_STDOUT = "Stopping notebook with id: n123\n"
    COMMAND_WITH_API_KEY_USED = [
        "notebooks",
        "stop",
        "--id", "n123",
        "--apiKey", "some_key",
    ]
    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Unable to stop instance: Invalid API token\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_and_print_notebook_id(self, post_patched):
        post_patched.return_value = MockResponse(example_responses.NOTEBOOK_GET_RESPONSE)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             data=None,
                                             files=None,
                                             params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, post_patched, get_patched):
        post_patched.return_value = MockResponse(example_responses.NOTEBOOK_GET_RESPONSE)
        get_patched.return_value = MockResponse(example_responses.NOTEBOOK_GET_RESPONSE)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_USED)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             data=None,
                                             files=None,
                                             params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_command_was_used_with_invalid_api_token(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN, result.exc_info
        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=self.EXPECTED_REQUEST_JSON,
                                        data=None,
                                        files=None,
                                        params=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, post_patched):
        post_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == "Unable to stop instance\n", result.exc_info
        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=self.EXPECTED_REQUEST_JSON,
                                        data=None,
                                        files=None,
                                        params=None)
        assert result.exit_code == 0


class TestListNotebookArtifacts(object):
    runner = CliRunner()
    URL = "https://api.paperspace.io/notebooks/artifactsList"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_get_request_with_all_parameters_for_a_list_of_artifacts(self, get_patched):
        get_patched.return_value = MockResponse()
        notebook_id = "some_notebook_id"
        result = self.runner.invoke(cli.cli,
                                    ["notebooks", "artifacts", "list", "--id", notebook_id, "--apiKey", "some_key",
                                     "--size",
                                     "--links",
                                     "--files", "foo"])

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params={"notebookId": notebook_id,
                                               "size": True,
                                               "links": True,
                                               "files": "foo"})
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
        get_patched.return_value = MockResponse()
        notebook_id = "some_notebook_id"
        result = self.runner.invoke(cli.cli,
                                    ["notebooks", "artifacts", "list", "--id", notebook_id, "--apiKey", "some_key"] + [
                                        option])

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params={"notebookId": notebook_id,
                                               param: True})
        assert result.exit_code == 0


class TestNotebooksDelete(object):
    URL = "https://api.paperspace.io/notebooks/v2/deleteNotebook"
    COMMAND = [
        "notebooks",
        "delete",
        "--id", "some_id",
    ]
    EXPECTED_REQUEST_JSON = {"notebookId": "some_id"}
    EXPECTED_STDOUT = "Notebook deleted\n"

    COMMAND_WITH_API_KEY_USED = [
        "notebooks",
        "delete",
        "--id", "some_id",
        "--apiKey", "some_key",
    ]

    COMMAND_WITH_OPTIONS_FILE_USED = ["notebooks", "delete", "--optionsFile", ]  # path added in test

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to delete resource: Invalid API token\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_and_print_notebook_id(self, post_patched):
        post_patched.return_value = MockResponse(status_code=204)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             data=None,
                                             files=None,
                                             params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=204)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_USED)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             data=None,
                                             files=None,
                                             params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_option_from_yaml_file(self, post_patched, notebooks_delete_config_path):
        post_patched.return_value = MockResponse(status_code=204)
        command = self.COMMAND_WITH_OPTIONS_FILE_USED[:] + [notebooks_delete_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             data=None,
                                             files=None,
                                             params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_command_was_used_with_invalid_api_token(self, get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=self.EXPECTED_REQUEST_JSON,
                                       data=None,
                                       files=None,
                                       params=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == "Failed to delete resource\n", result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=self.EXPECTED_REQUEST_JSON,
                                       data=None,
                                       files=None,
                                       params=None)
        assert result.exit_code == 0


class TestNotebooksdetails(object):
    URL = "https://api.paperspace.io/notebooks/getNotebook"
    COMMAND = ["notebooks", "details", "--id", "some_id"]
    EXPECTED_STDOUT = """+---------+-----------------------------------+
| Name    | some_name                         |
+---------+-----------------------------------+
| ID      | ngw7piq9                          |
| Project | prg284tu2                         |
| VM Type | K80                               |
| State   | Running                           |
| FQDN    | ngw7piq9.dgradient.paperspace.com |
| Tags    |                                   |
+---------+-----------------------------------+
"""
    EXPECTED_STDOUT_WITH_TAGS = """+---------+-----------------------------------+
| Name    | some_name                         |
+---------+-----------------------------------+
| ID      | ngw7piq9                          |
| Project | prg284tu2                         |
| VM Type | K80                               |
| State   | Running                           |
| FQDN    | ngw7piq9.dgradient.paperspace.com |
| Tags    | tag1, tag2                        |
+---------+-----------------------------------+
"""
    RESPONSE_JSON = example_responses.NOTEBOOK_GET_RESPONSE
    RESPONSE_JSON_WITH_TAGS = example_responses.NOTEBOOK_GET_RESPONSE_WITH_TAGS

    COMMAND_WITH_API_KEY_USED = ["notebooks", "details", "--id", "some_id", "--apiKey", "some_key"]

    COMMAND_WITH_OPTIONS_FILE_USED = ["notebooks", "details", "--optionsFile", ]  # path added in test

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to fetch data: Invalid API token\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_post_request_and_print_notebook_details(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json={"notebookId": "some_id"},
                                             params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_post_request_and_print_notebook_details_with_tags(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_TAGS)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WITH_TAGS, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json={"notebookId": "some_id"},
                                             params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_USED)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json={"notebookId": "some_id"},
                                             params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_option_from_yaml_file(self, post_patched, notebooks_show_config_path):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE_USED[:] + [notebooks_show_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json={"notebookId": "some_id"},
                                             params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_command_was_used_with_invalid_api_token(self, get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json={"notebookId": "some_id"},
                                       params=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == "Failed to fetch data\n", result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json={"notebookId": "some_id"},
                                       params=None)
        assert result.exit_code == 0


class TestNotebooksList(object):
    URL = "https://api.paperspace.io/notebooks/getNotebooks"
    COMMAND = ["notebooks", "list"]
    COMMAND_WITH_FILTERING_BY_TAGS = [
        "notebooks", "list",
        "--tag", "tag1",
        "--tag", "tag2",
    ]
    EXPECTED_STDOUT = """+--------------------+----------+
| Name               | ID       |
+--------------------+----------+
| job 1              | n1vmfj6x |
| job 1              | nhdf8zf3 |
| My Notebook 123    | nslk5r03 |
| My Notebook 123    | ng9a3tp4 |
| some_name          | ngw7piq9 |
| some_notebook_name | n8h0d5lf |
| some_notebook_name | nl0b6cn0 |
| some_notebook_name | njmq1zju |
| some_notebook_name | nfcuwqu5 |
+--------------------+----------+

"""
    RESPONSE_JSON = example_responses.NOTEBOOKS_LIST_RESPONSE_JSON

    COMMAND_WITH_API_KEY_USED = ["notebooks", "list", "--apiKey", "some_key"]

    COMMAND_WITH_OPTIONS_FILE_USED = ["notebooks", "list", "--optionsFile", ]  # path added in test

    EXPECTED_FILTERS = {
        "filter": {
            "where": {
                "dtDeleted": None,
            },
            "limit": 20,
            "order": "jobId desc",
            "offset": 0,
        },
    }

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to fetch data: Invalid API token\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_post_request_and_print_notebook_details(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=None,
                                             params=mock.ANY)
        params = post_patched.call_args.kwargs["params"]
        filter_params = params["filter"]
        filter_params = json.loads(filter_params)
        assert filter_params == self.EXPECTED_FILTERS
        assert "tagFilter[0]" not in params

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_post_request_and_print_notebook_details_when_filtering_by_tags(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_FILTERING_BY_TAGS)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=None,
                                             params=mock.ANY)
        params = post_patched.call_args.kwargs["params"]
        filter_params = params["filter"]
        filter_params = json.loads(filter_params)
        assert filter_params == self.EXPECTED_FILTERS
        assert "tagFilter[0]" in params
        assert params["tagFilter[0]"] in ("tag1", "tag2")
        assert params["tagFilter[1]"] in ("tag1", "tag2")
        assert params["tagFilter[0]"] != params["tagFilter[1]"]

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_USED)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=mock.ANY)
        params = get_patched.call_args.kwargs["params"]
        filter_params = params["filter"]
        filter_params = json.loads(filter_params)
        assert filter_params == self.EXPECTED_FILTERS

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_option_from_yaml_file(self, get_patched, notebooks_list_config_path):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE_USED[:] + [notebooks_list_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=mock.ANY)
        params = get_patched.call_args.kwargs["params"]
        filter_params = params["filter"]
        filter_params = json.loads(filter_params)
        assert filter_params == self.EXPECTED_FILTERS

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_command_was_used_with_invalid_api_token(self, get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=mock.ANY)
        params = get_patched.call_args.kwargs["params"]
        filter_params = params["filter"]
        filter_params = json.loads(filter_params)
        assert filter_params == self.EXPECTED_FILTERS
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == "Failed to fetch data\n", result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=mock.ANY)
        params = get_patched.call_args.kwargs["params"]
        filter_params = params["filter"]
        filter_params = json.loads(filter_params)
        assert filter_params == self.EXPECTED_FILTERS
        assert result.exit_code == 0


class TestNotebooksMetricsGetCommand(object):
    GET_NOTEBOOK_URL = "https://api.paperspace.io/notebooks/getNotebook"
    GET_METRICS_URL = "https://aws-testing.paperspace.io/metrics/api/v1/range"
    BASIC_OPTIONS_COMMAND = [
        "notebooks", "metrics", "get",
        "--id", "ngw7piq9",
    ]
    ALL_OPTIONS_COMMAND = [
        "notebooks", "metrics", "get",
        "--id", "ngw7piq9",
        "--metric", "gpuMemoryFree",
        "--metric", "gpuMemoryUsed",
        "--interval", "20s",
        "--start", "2020-04-01",
        "--end", "2020-04-02 21:37:00",
        "--apiKey", "some_key",
    ]
    FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE = [
        "notebooks", "metrics", "get",
        "--optionsFile",  # path added in test,
    ]

    GET_NOTEBOOK_REQUEST_JSON = {"notebookId": "ngw7piq9"}
    BASIC_COMMAND_GET_METRICS_REQUEST_PARAMS = {
        "start": "2019-09-03T11:10:36Z",
        "handle": "ngw7piq9",
        "interval": "30s",
        "charts": "cpuPercentage,memoryUsage",
        "objecttype": "notebook",
    }
    ALL_COMMANDS_GET_METRICS_REQUEST_PARAMS = {
        "start": "2020-04-01T00:00:00Z",
        "handle": "ngw7piq9",
        "interval": "20s",
        "charts": "gpuMemoryFree,gpuMemoryUsed",
        "objecttype": "notebook",
        "end": "2020-04-02T21:37:00Z",
    }

    GET_NOTEBOOK_RESPONSE_JSON = example_responses.NOTEBOOK_GET_RESPONSE
    GET_METRICS_RESPONSE_JSON = example_responses.NOTEBOOKS_METRICS_GET_RESPONSE

    EXPECTED_STDOUT = """{
  "cpuPercentage": {
    "npmnnm6e": [
      {
        "time_stamp": 1587993000, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587993030, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587993060, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587993090, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587993120, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587993150, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587993180, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587993210, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587993240, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587993270, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587993300, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587993330, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587993360, 
        "value": "0"
      }
    ]
  }, 
  "memoryUsage": {
    "npmnnm6e": [
      {
        "time_stamp": 1587992970, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587993000, 
        "value": "782336"
      }, 
      {
        "time_stamp": 1587993030, 
        "value": "782336"
      }, 
      {
        "time_stamp": 1587993060, 
        "value": "782336"
      }, 
      {
        "time_stamp": 1587993090, 
        "value": "782336"
      }, 
      {
        "time_stamp": 1587993120, 
        "value": "782336"
      }, 
      {
        "time_stamp": 1587993150, 
        "value": "782336"
      }, 
      {
        "time_stamp": 1587993180, 
        "value": "782336"
      }, 
      {
        "time_stamp": 1587993210, 
        "value": "782336"
      }, 
      {
        "time_stamp": 1587993240, 
        "value": "782336"
      }, 
      {
        "time_stamp": 1587993270, 
        "value": "782336"
      }, 
      {
        "time_stamp": 1587993300, 
        "value": "782336"
      }, 
      {
        "time_stamp": 1587993330, 
        "value": "782336"
      }, 
      {
        "time_stamp": 1587993360, 
        "value": "782336"
      }
    ]
  }
}
"""

    EXPECTED_STDOUT_WHEN_INVALID_API_KEY_WAS_USED = "Failed to fetch data: Invalid API token\n"
    EXPECTED_STDOUT_WHEN_EXPERIMENT_WAS_NOT_FOUND = "Failed to fetch data: Not found. " \
                                                    "Please contact support@paperspace.com for help.\n"
    EXPECTED_STDOUT_WHEN_NO_METRICS_WERE_FOUND = """{
  "cpuPercentage": null, 
  "memoryUsage": null
}
"""
    EXPECTED_STDOUT_WHEN_ERROR_CODE_WAS_RETURNED_WITHOUT_ERROR_MESSAGE = "Failed to fetch data\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_all_available_metrics_when_metrics_get_command_was_used_with_basic_options(self, get_patched):
        get_patched.side_effect = [
            MockResponse(self.GET_NOTEBOOK_RESPONSE_JSON),
            MockResponse(self.GET_METRICS_RESPONSE_JSON),
        ]

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        assert json.loads(result.output.strip()) == json.loads(self.EXPECTED_STDOUT.strip()), \
            str(result.output) + str(result.exc_info)
        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_NOTEBOOK_URL,
                    json=self.GET_NOTEBOOK_REQUEST_JSON,
                    params=None,
                    headers=EXPECTED_HEADERS,
                ),
                mock.call(
                    self.GET_METRICS_URL,
                    json=None,
                    params=self.BASIC_COMMAND_GET_METRICS_REQUEST_PARAMS,
                    headers=EXPECTED_HEADERS,
                ),
            ]
        )

        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_metrics_when_metrics_get_command_was_used_with_all_options(self, get_patched):
        get_patched.side_effect = [
            MockResponse(self.GET_NOTEBOOK_RESPONSE_JSON),
            MockResponse(self.GET_METRICS_RESPONSE_JSON),
        ]

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        # comparing objects instead of strings because Py2 and Py3 produce slightly different outputs
        assert json.loads(result.output.strip()) == json.loads(self.EXPECTED_STDOUT.strip()), result.exc_info
        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_NOTEBOOK_URL,
                    json=self.GET_NOTEBOOK_REQUEST_JSON,
                    params=None,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
                mock.call(
                    self.GET_METRICS_URL,
                    json=None,
                    params=self.ALL_COMMANDS_GET_METRICS_REQUEST_PARAMS,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
            ]
        )

        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_metrics_when_metrics_get_was_executed_and_options_file_was_used(
            self, get_patched, notebooks_metrics_get_config_path):
        get_patched.side_effect = [
            MockResponse(self.GET_NOTEBOOK_RESPONSE_JSON),
            MockResponse(self.GET_METRICS_RESPONSE_JSON),
        ]
        command = self.FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE[:] + [notebooks_metrics_get_config_path]
        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        # comparing objects instead of strings because Py2 and Py3 produce slightly different outputs
        assert json.loads(result.output.strip()) == json.loads(self.EXPECTED_STDOUT.strip()), result.exc_info
        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_NOTEBOOK_URL,
                    json=self.GET_NOTEBOOK_REQUEST_JSON,
                    params=None,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
                mock.call(
                    self.GET_METRICS_URL,
                    json=None,
                    params=self.ALL_COMMANDS_GET_METRICS_REQUEST_PARAMS,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
            ]
        )

        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_invalid_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse({"status": 400, "message": "Invalid API token"},
                                                status_code=403)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_INVALID_API_KEY_WAS_USED, result.exc_info

        get_patched.assert_called_once_with(
            self.GET_NOTEBOOK_URL,
            json=self.GET_NOTEBOOK_REQUEST_JSON,
            params=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_deployment_was_not_found(self, get_patched):
        get_patched.side_effect = [
            MockResponse({"error": {"name": "ApplicationError", "status": 404,
                                    "message": "Not found. Please contact support@paperspace.com for help."}},
                         status_code=404),
        ]

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_EXPERIMENT_WAS_NOT_FOUND, result.exc_info

        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_NOTEBOOK_URL,
                    json=self.GET_NOTEBOOK_REQUEST_JSON,
                    params=None,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
            ]
        )

        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_message_when_was_no_metrics_were_returned(self, get_patched):
        get_patched.side_effect = [
            MockResponse(self.GET_NOTEBOOK_RESPONSE_JSON),
            MockResponse(example_responses.NOTEBOOKS_METRICS_GET_RESPONSE_WHEN_NO_METRICS_WERE_FOUND),
        ]

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert json.loads(result.output.strip()) == json.loads(self.EXPECTED_STDOUT_WHEN_NO_METRICS_WERE_FOUND.strip()) \
            , str(result.output) + str(result.exc_info)
        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_NOTEBOOK_URL,
                    json=self.GET_NOTEBOOK_REQUEST_JSON,
                    params=None,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
                mock.call(
                    self.GET_METRICS_URL,
                    json=None,
                    params=self.ALL_COMMANDS_GET_METRICS_REQUEST_PARAMS,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
            ]
        )

        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_error_code_was_returned_without_error_message(self, get_patched):
        get_patched.side_effect = [
            MockResponse(self.GET_NOTEBOOK_RESPONSE_JSON),
            MockResponse(status_code=500),
        ]

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_ERROR_CODE_WAS_RETURNED_WITHOUT_ERROR_MESSAGE, result.exc_info

        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_NOTEBOOK_URL,
                    json=self.GET_NOTEBOOK_REQUEST_JSON,
                    params=None,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
                mock.call(
                    self.GET_METRICS_URL,
                    json=None,
                    params=self.ALL_COMMANDS_GET_METRICS_REQUEST_PARAMS,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
            ]
        )

        assert result.exit_code == 0, result.exc_info


class TestNotebooksMetricsStreamCommand(object):
    GET_NOTEBOOK_URL = "https://api.paperspace.io/notebooks/getNotebook"
    GET_METRICS_URL = "https://aws-testing.paperspace.io/metrics/api/v1/stream"
    BASIC_OPTIONS_COMMAND = [
        "notebooks", "metrics", "stream",
        "--id", "ngw7piq9",
    ]
    ALL_OPTIONS_COMMAND = [
        "notebooks", "metrics", "stream",
        "--id", "ngw7piq9",
        "--metric", "gpuMemoryFree",
        "--metric", "gpuMemoryUsed",
        "--interval", "20s",
        "--apiKey", "some_key",
    ]
    ALL_OPTIONS_COMMAND_WITH_OPTIONS_FILE = [
        "notebooks", "metrics", "stream",
        "--optionsFile",  # path added in test,
    ]

    GET_NOTEBOOK_REQUEST_JSON = {"notebookId": "ngw7piq9"}
    BASIC_COMMAND_CHART_DESCRIPTOR = '{"chart_names": ["cpuPercentage", "memoryUsage"], "handles": ["ngw7piq9"' \
                                     '], "object_type": "notebook", "poll_interval": "30s"}'

    ALL_COMMANDS_CHART_DESCRIPTOR = '{"chart_names": ["gpuMemoryFree", "gpuMemoryUsed"], "handles": ["ngw7piq9' \
                                    '"], "object_type": "notebook", "poll_interval": "20s"}'

    GET_NOTEBOOK_RESPONSE_JSON = example_responses.NOTEBOOK_GET_RESPONSE
    GET_NOTEBOOK_RESPONSE_JSON_WHEN_NOTEBOOK_NOT_FOUND = {
        "error": {
            "name": "ApplicationError",
            "status": 404,
            "message": "Not found. Please contact support@paperspace.com for help.",
        },
    }

    EXPECTED_TABLE_1 = """+----------+---------------+-------------+
| Pod      | cpuPercentage | memoryUsage |
+----------+---------------+-------------+
| nrwed38p |               | 54013952    |
+----------+---------------+-------------+"""
    EXPECTED_TABLE_2 = """+----------+----------------------+-------------+
| Pod      | cpuPercentage        | memoryUsage |
+----------+----------------------+-------------+
| nrwed38p | 0.006907773333334353 | 54013952    |
+----------+----------------------+-------------+"""
    EXPECTED_TABLE_3 = """+----------+----------------------+-------------+
| Pod      | cpuPercentage        | memoryUsage |
+----------+----------------------+-------------+
| nrwed38p | 0.006907773333334353 | 12345667    |
+----------+----------------------+-------------+"""

    ALL_OPTIONS_EXPECTED_TABLE_1 = """+----------+---------------+---------------+
| Pod      | gpuMemoryFree | gpuMemoryUsed |
+----------+---------------+---------------+
| nrwed38p | 1234          |               |
+----------+---------------+---------------+"""
    ALL_OPTIONS_EXPECTED_TABLE_2 = """+----------+---------------+---------------+
| Pod      | gpuMemoryFree | gpuMemoryUsed |
+----------+---------------+---------------+
| nrwed38p | 1234          | 32            |
+----------+---------------+---------------+"""
    ALL_OPTIONS_EXPECTED_TABLE_3 = """+----------+---------------+---------------+
| Pod      | gpuMemoryFree | gpuMemoryUsed |
+----------+---------------+---------------+
| nrwed38p | 2345          | 32            |
+----------+---------------+---------------+"""

    EXPECTED_STDOUT_WHEN_INVALID_API_KEY_WAS_USED = "Failed to fetch data: Incorrect API Key provided\nForbidden\n"
    EXPECTED_STDOUT_WHEN_DEPLOYMENT_WAS_NOT_FOUND = "Failed to fetch data: Not found. Please contact " \
                                                    "support@paperspace.com for help.\n"

    @mock.patch("gradient.commands.common.TerminalPrinter")
    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_all_available_metrics_when_metrics_get_command_was_used_with_basic_options(
            self, get_patched, create_ws_connection_patched, terminal_printer_cls_patched,
            basic_options_metrics_stream_websocket_connection_iterator):
        get_patched.return_value = MockResponse(self.GET_NOTEBOOK_RESPONSE_JSON)

        ws_connection_instance_mock = mock.MagicMock()
        ws_connection_instance_mock.__iter__ = basic_options_metrics_stream_websocket_connection_iterator
        create_ws_connection_patched.return_value = ws_connection_instance_mock

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        terminal_printer_cls_patched().init.assert_called_once()
        terminal_printer_cls_patched().rewrite_screen.assert_has_calls([
            mock.call(self.EXPECTED_TABLE_1),
            mock.call(self.EXPECTED_TABLE_2),
            mock.call(self.EXPECTED_TABLE_3),
        ])
        terminal_printer_cls_patched().cleanup.assert_called_once()

        get_patched.assert_called_once_with(
            self.GET_NOTEBOOK_URL,
            json=self.GET_NOTEBOOK_REQUEST_JSON,
            params=None,
            headers=EXPECTED_HEADERS,
        )
        ws_connection_instance_mock.send.assert_called_once_with(self.BASIC_COMMAND_CHART_DESCRIPTOR)
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.commands.common.TerminalPrinter")
    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_metrics_when_metrics_get_command_was_used_with_all_options(
            self, get_patched, create_ws_connection_patched, terminal_printer_cls_patched,
            all_options_metrics_stream_websocket_connection_iterator):
        get_patched.return_value = MockResponse(self.GET_NOTEBOOK_RESPONSE_JSON)

        ws_connection_instance_mock = mock.MagicMock()
        ws_connection_instance_mock.__iter__ = all_options_metrics_stream_websocket_connection_iterator
        create_ws_connection_patched.return_value = ws_connection_instance_mock

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        terminal_printer_cls_patched().init.assert_called_once()
        terminal_printer_cls_patched().rewrite_screen.assert_has_calls([
            mock.call(self.ALL_OPTIONS_EXPECTED_TABLE_1),
            mock.call(self.ALL_OPTIONS_EXPECTED_TABLE_2),
            mock.call(self.ALL_OPTIONS_EXPECTED_TABLE_3),
        ])
        terminal_printer_cls_patched().cleanup.assert_called_once()

        get_patched.assert_called_once_with(
            self.GET_NOTEBOOK_URL,
            json=self.GET_NOTEBOOK_REQUEST_JSON,
            params=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        ws_connection_instance_mock.send.assert_called_once_with(self.ALL_COMMANDS_CHART_DESCRIPTOR)
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.commands.common.TerminalPrinter")
    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_metrics_when_metrics_get_was_executed_and_options_file_was_used(
            self, get_patched, create_ws_connection_patched, terminal_printer_cls_patched,
            all_options_metrics_stream_websocket_connection_iterator,
            notebooks_metrics_stream_config_path):
        get_patched.return_value = MockResponse(self.GET_NOTEBOOK_RESPONSE_JSON)
        ws_connection_instance_mock = mock.MagicMock()
        ws_connection_instance_mock.__iter__ = all_options_metrics_stream_websocket_connection_iterator
        create_ws_connection_patched.return_value = ws_connection_instance_mock

        command = self.ALL_OPTIONS_COMMAND_WITH_OPTIONS_FILE[:] + [notebooks_metrics_stream_config_path]
        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        terminal_printer_cls_patched().init.assert_called_once()
        terminal_printer_cls_patched().rewrite_screen.assert_has_calls([
            mock.call(self.ALL_OPTIONS_EXPECTED_TABLE_1),
            mock.call(self.ALL_OPTIONS_EXPECTED_TABLE_2),
            mock.call(self.ALL_OPTIONS_EXPECTED_TABLE_3),
        ])
        terminal_printer_cls_patched().cleanup.assert_called_once()

        get_patched.assert_called_once_with(
            self.GET_NOTEBOOK_URL,
            json=self.GET_NOTEBOOK_REQUEST_JSON,
            params=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        ws_connection_instance_mock.send.assert_called_once_with(self.ALL_COMMANDS_CHART_DESCRIPTOR)
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.commands.common.TerminalPrinter")
    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_invalid_api_key_was_used(
            self, get_patched, create_ws_connection_patched, terminal_printer_cls_patched):
        get_patched.return_value = MockResponse({"status": 400, "message": "Invalid API token"}, 400)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert "Failed to fetch data: Invalid API token\n" == result.output, result.exc_info

        get_patched.assert_called_once_with(
            self.GET_NOTEBOOK_URL,
            json=self.GET_NOTEBOOK_REQUEST_JSON,
            params=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        create_ws_connection_patched.assert_not_called()
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.commands.common.TerminalPrinter")
    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_deployment_was_not_found(
            self, get_patched, create_ws_connection_patched, terminal_printer_cls_patched):
        get_patched.return_value = MockResponse(self.GET_NOTEBOOK_RESPONSE_JSON_WHEN_NOTEBOOK_NOT_FOUND, 404)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_DEPLOYMENT_WAS_NOT_FOUND, result.exc_info

        get_patched.assert_called_once_with(
            self.GET_NOTEBOOK_URL,
            json=self.GET_NOTEBOOK_REQUEST_JSON,
            params=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        create_ws_connection_patched.assert_not_called()
        assert result.exit_code == 0, result.exc_info
