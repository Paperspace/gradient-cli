import mock
from click.testing import CliRunner

import gradient.api_sdk.clients.http_client
from gradient.cli import cli
from tests import MockResponse, example_responses


class TestNotebooksCreate(object):
    URL = "https://api.paperspace.io/notebooks/createNotebook"
    COMMAND = [
        "notebooks",
        "create",
        "--vmTypeId", "25",
        "--containerId", "123",
        "--clusterId", "321"
    ]
    EXPECTED_REQUEST_JSON = {"vmTypeId": 25, "containerId": 123, "clusterId": 321}
    EXPECTED_RESPONSE_JSON = {
        "handle": "some_id",
        "notebookToken": None,
        "jobId": 20163,
        "isPublic": False,
        "id": 1811,
        "containerId": 123,
    }
    EXPECTED_STDOUT = """Created new notebook with id: some_id\n"""

    COMMAND_WITH_API_KEY_USED = [
        "notebooks",
        "create",
        "--vmTypeId", "25",
        "--containerId", "123",
        "--clusterId", "321",
        "--apiKey", "some_key",
    ]

    COMMAND_WITH_ALL_OPTIONS = [
        "notebooks",
        "create",
        "--vmTypeId", "25",
        "--containerId", "123",
        "--clusterId", "321",
        "--name", "some_notebook_name",
        "--registryUsername", "some_username",
        "--registryPassword", "some_password",
        "--defaultEntrypoint", "some_entrypoint",
        "--containerUser", "some_container_user",
        "--shutdownTimeout", "8",
        "--isPreemptible",
    ]
    EXPECTED_REQUEST_JSON_WITH_ALL_OPTIONS = {
        "vmTypeId": 25,
        "containerId": 123,
        "clusterId": 321,
        "name": "some_notebook_name",
        "registryUsername": "some_username",
        "registryPassword": "some_password",
        "defaultEntrypoint": "some_entrypoint",
        "containerUser": "some_container_user",
        "shutdownTimeout": 8,
        "isPreemptible": True,
    }
    COMMAND_WITH_OPTIONS_FILE_USED = ["notebooks", "create", "--optionsFile", ]  # path added in test

    EXPECTED_HEADERS = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to create resource: Invalid API token\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_and_print_notebook_id(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             data=None,
                                             files=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_USED)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             data=None,
                                             files=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_and_print_notebook_id_when_all_options_were_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_ALL_OPTIONS)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON_WITH_ALL_OPTIONS,
                                             data=None,
                                             files=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_option_from_yaml_file(self, post_patched, notebooks_create_config_path):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE_USED[:] + [notebooks_create_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON_WITH_ALL_OPTIONS,
                                             data=None,
                                             files=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_command_was_used_with_invalid_api_token(self,
                                                                                           get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.EXPECTED_REQUEST_JSON,
                                       data=None,
                                       files=None,
                                       params=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self,
                                                                                                        get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == "Failed to create resource\n", result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.EXPECTED_REQUEST_JSON,
                                       data=None,
                                       files=None,
                                       params=None)
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

    EXPECTED_HEADERS = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to delete resource: Invalid API token\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_and_print_notebook_id(self, post_patched):
        post_patched.return_value = MockResponse(status_code=204)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             data=None,
                                             files=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=204)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_USED)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             data=None,
                                             files=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_option_from_yaml_file(self, post_patched, notebooks_delete_config_path):
        post_patched.return_value = MockResponse(status_code=204)
        command = self.COMMAND_WITH_OPTIONS_FILE_USED[:] + [notebooks_delete_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             data=None,
                                             files=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_command_was_used_with_invalid_api_token(self, get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
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
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.EXPECTED_REQUEST_JSON,
                                       data=None,
                                       files=None,
                                       params=None)
        assert result.exit_code == 0


class TestNotebooksShow(object):
    URL = "https://api.paperspace.io/notebooks/some_id/getNotebook"
    COMMAND = ["notebooks", "show", "--id", "some_id"]
    EXPECTED_STDOUT = """+---------+-----------------------------------+
| Name    | some_name                         |
+---------+-----------------------------------+
| ID      | ngw7piq9                          |
| VM Type | K80                               |
| State   | Running                           |
| FQDN    | ngw7piq9.dgradient.paperspace.com |
+---------+-----------------------------------+
"""
    RESPONSE_JSON = example_responses.NOTEBOOK_GET_RESPONSE

    COMMAND_WITH_API_KEY_USED = ["notebooks", "show", "--id", "some_id", "--apiKey", "some_key"]

    COMMAND_WITH_OPTIONS_FILE_USED = ["notebooks", "show", "--optionsFile", ]  # path added in test

    EXPECTED_HEADERS = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to fetch data: Invalid API token\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_post_request_and_print_notebook_details(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_USED)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_option_from_yaml_file(self, post_patched, notebooks_show_config_path):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE_USED[:] + [notebooks_show_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_command_was_used_with_invalid_api_token(self, get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == "Failed to fetch data\n", result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=None)
        assert result.exit_code == 0


class TestNotebooksList(object):
    URL = "https://api.paperspace.io/notebooks/getNotebooks"
    COMMAND = ["notebooks", "list"]
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

    EXPERCTED_REQUEST_JSON = {
        "filter": {
            "filter": {
                "where": {
                    "dtDeleted": None,
                },
                "limit": 11,
                "order": "jobId desc",
                "offset": 0,
            },
        },
    }

    EXPECTED_HEADERS = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to fetch data: Invalid API token\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_post_request_and_print_notebook_details(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.EXPERCTED_REQUEST_JSON,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_USED)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPERCTED_REQUEST_JSON,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_option_from_yaml_file(self, post_patched, notebooks_list_config_path):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE_USED[:] + [notebooks_list_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPERCTED_REQUEST_JSON,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_command_was_used_with_invalid_api_token(self, get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.EXPERCTED_REQUEST_JSON,
                                       params=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == "Failed to fetch data\n", result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.EXPERCTED_REQUEST_JSON,
                                       params=None)
        assert result.exit_code == 0
