import mock
from click.testing import CliRunner

import gradient.api_sdk.clients.http_client
from gradient.api_sdk.clients.http_client import default_headers
from gradient.cli import cli
from tests import example_responses, MockResponse


class TestListProjects(object):
    URL = "https://api.paperspace.io/projects/"
    EXPECTED_HEADERS = default_headers.copy()
    BASIC_COMMAND = ["projects", "list"]
    # TODO: change to `REQUEST_JSON = None` or whatever works when PS_API is fixed
    EXPECTED_RESPONSE_JSON = example_responses.LIST_PROJECTS_RESPONSE
    EXPECTED_STDOUT = """+-----------+-------------------+------------+----------------------------+
| ID        | Name              | Repository | Created                    |
+-----------+-------------------+------------+----------------------------+
| prq70zy79 | test_project      | None       | 2019-03-18 13:24:46.666000 |
| prmr22ve0 | keton             | None       | 2019-03-25 14:50:43.202000 |
| przhbct98 | paperspace-python | None       | 2019-04-04 15:12:34.229000 |
+-----------+-------------------+------------+----------------------------+
"""

    BASIC_COMMAND_WITH_API_KEY = ["projects", "list", "--apiKey", "some_key"]
    COMMAND_WITH_OPTIONS_FILE = ["projects", "list", "--optionsFile", ]  # path added in test

    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to fetch data: Invalid API token\n"

    RESPONSE_JSON_WHEN_NO_PROJECTS_WERE_FOUND = {"data": [], "meta": {"totalItems": 0}}
    EXPECTED_STDOUT_WHEN_NO_PROJECTS_WERE_FOUND = "No data found\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_and_print_table_when_projects_list_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_projects_list_was_used_with_api_key_option(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, get_patched, projects_list_config_path):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [projects_list_config_path]

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_projects_list_was_used_with_wrong_api_key(self, get_patched):
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
    def test_should_print_error_message_when_no_project_was_not_found(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_NO_PROJECTS_WERE_FOUND,
                                                status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT_WHEN_NO_PROJECTS_WERE_FOUND
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


class TestCreateProject(object):
    URL = "https://api.paperspace.io/projects/"
    COMMAND = [
        "projects", "create",
        "--name", "some_name",
    ]
    EXPECTED_REQUEST_JSON = {"name": "some_name"}
    EXPECTED_RESPONSE_JSON = {
        "name": "some_name",
        "handle": "pru5a4dnu",
        "dtCreated": "2019-06-10T12:20:17.173Z",
        "dtDeleted": None,
        "lastJobSeqNum": 0,
        "repoNodeId": None,
        "repoName": None,
        "repoUrl": None,
    }

    COMMAND_WHEN_ALL_PARAMETERS_WERE_USED = [
        "projects", "create",
        "--name", "some_name",
        "--repositoryName", "some_repository_name",
        "--repositoryUrl", "some_repository_url",
    ]
    COMMAND_WITH_OPTIONS_FILE = ["projects", "create", "--optionsFile", ]  # path added in test

    EXPECTED_REQUEST_JSON_WHEN_ALL_PARAMETERS_WERE_USED = {
        "repoUrl": "some_repository_url",
        "name": "some_name",
        "repoName": "some_repository_name",
    }
    EXPECTED_RESPONSE_JSON_WHEN_ALL_PARAMETERS_WERE_USED = {
        "name": "mnist",
        "handle": "pru5a4dnu",
        "dtCreated": "2019-06-10T12:25:59.464Z",
        "dtDeleted": None,
        "lastJobSeqNum": 0,
        "repoNodeId": None,
        "repoName": "mnist-sample",
        "repoUrl": "https://github.com/Paperspace/mnist-sample",
    }

    EXPECTED_HEADERS = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"
    EXPECTED_STDOUT = "Project created with ID: pru5a4dnu\n"

    EXPECTED_RESPONSE_JSON_WITH_ERROR = {
        "error": {
            "name": "ValidationError",
            "status": 422,
            "message": "The `project` instance is not valid. Details: `name` can't be blank (value: undefined).",
            "statusCode": 422,
            "details": {
                "context": "project",
                "codes": {"name": ["presence"]},
                "messages": {"name": ["can't be blank"]},
            },
        },
    }
    EXPECTED_STDOUT_WHEN_ERROR_RECEIVED = "Failed to create resource: The `project` instance is not valid. " \
                                          "Details: `name` can't be blank (value: undefined).\n"

    COMMAND_WITH_API_KEY_PARAMETER_USED = [
        "projects", "create",
        "--name", "some_name",
        "--apiKey", "some_key",
    ]

    EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WHEN_WRONG_API_KEY_WAS_USED = "Failed to create resource: Invalid API token\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_and_print_proper_message_when_create_command_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON_WHEN_ALL_PARAMETERS_WERE_USED, 201)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.output == self.EXPECTED_STDOUT
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_and_print_proper_message_when_create_command_was_used_with_all_options(
            self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON_WHEN_ALL_PARAMETERS_WERE_USED, 201)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WHEN_ALL_PARAMETERS_WERE_USED)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON_WHEN_ALL_PARAMETERS_WERE_USED,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.output == self.EXPECTED_STDOUT
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_replace_api_key_in_headers_when_api_key_parameter_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON, 201)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_PARAMETER_USED)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.output == self.EXPECTED_STDOUT
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, post_patched, projects_create_config_path):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON, 201)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [projects_create_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON_WHEN_ALL_PARAMETERS_WERE_USED,
                                             params=None,
                                             files=None,
                                             data=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_proper_message_when_error_message_received(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON_WITH_ERROR, 400)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.output == self.EXPECTED_STDOUT_WHEN_ERROR_RECEIVED

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED, 403)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.output == self.EXPECTED_STDOUT_WHEN_WRONG_API_KEY_WAS_USED
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_request_and_print_proper_message_when_error_code_returned_without_json_data(self,
                                                                                                     post_patched):
        post_patched.return_value = MockResponse(status_code=500)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.output == "Failed to create resource\n"
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"
