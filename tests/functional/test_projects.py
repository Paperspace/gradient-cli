import mock
from click.testing import CliRunner

from gradient.api_sdk.clients.http_client import default_headers
from gradient.cli import cli
from tests import example_responses, MockResponse

EXPECTED_HEADERS = default_headers.copy()
EXPECTED_HEADERS["ps_client_name"] = "gradient-cli"

EXPECTED_HEADERS_WITH_CHANGED_API_KEY = EXPECTED_HEADERS.copy()
EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"


class TestListProjects(object):
    URL = "https://api.paperspace.io/projects/"
    EXPECTED_PARAMS = {
        "filter": """{"offset":0,"where":{"dtDeleted":null},"order":"dtCreated desc"}"""
    }
    EXPECTED_PARAMS_WITH_FILTERING_BY_TAGS = {
        "filter": """{"offset":0,"where":{"dtDeleted":null},"order":"dtCreated desc"}""",
        "tagFilter": ("some_tag", "some_tag_2"),
    }
    BASIC_COMMAND = ["projects", "list"]
    BASIC_COMMAND_WITH_FILTERING_BY_TAGS = ["projects", "list", "--tag", "some_tag", "--tag", "some_tag_2"]
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
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.EXPECTED_PARAMS)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_and_print_table_when_projects_list_was_used_with_filtering_by_tags(
            self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_FILTERING_BY_TAGS)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.EXPECTED_PARAMS_WITH_FILTERING_BY_TAGS)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_projects_list_was_used_with_api_key_option(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.EXPECTED_PARAMS)
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
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.EXPECTED_PARAMS)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_projects_list_was_used_with_wrong_api_key(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.EXPECTED_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_error_message_when_no_project_was_not_found(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_NO_PROJECTS_WERE_FOUND,
                                                status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.EXPECTED_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WHEN_NO_PROJECTS_WERE_FOUND
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.EXPECTED_PARAMS)
        assert result.output == "Failed to fetch data\n"
        assert result.exit_code == 0


class TestCreateProject(object):
    URL = "https://api.paperspace.io/projects/"
    TAGS_URL = "https://api.paperspace.io/entityTags/updateTags"
    COMMAND = [
        "projects", "create",
        "--name", "some_name",
    ]
    COMMAND_WITH_TAGS = [
        "projects", "create",
        "--name", "some_name",
        "--tag", "test0",
        "--tag", "test1",
        "--tags", "test2,test3",
    ]
    EXPECTED_REQUEST_JSON = {"name": "some_name"}
    TAGS_JSON = {
        "entity": "project",
        "entityId": "pru5a4dnu",
        "tags": ["test0", "test1", "test2", "test3"]
    }
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
    UPDATE_TAGS_RESPONSE_JSON_200 = example_responses.UPDATE_TAGS_RESPONSE

    EXPECTED_STDOUT = "Project created with ID: pru5a4dnu\n" \
                      "https://console.paperspace.com/projects/pru5a4dnu\n"

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
                                             headers=EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.output == self.EXPECTED_STDOUT
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_and_print_proper_message_when_create_command_was_used_with_all_options(
            self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON_WHEN_ALL_PARAMETERS_WERE_USED, 201)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WHEN_ALL_PARAMETERS_WERE_USED)

        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON_WHEN_ALL_PARAMETERS_WERE_USED,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.output == self.EXPECTED_STDOUT
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_replace_api_key_in_headers_when_api_key_parameter_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON, 201)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_PARAMETER_USED)

        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.output == self.EXPECTED_STDOUT
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, post_patched, projects_create_config_path):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON, 201)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [projects_create_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
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
                                             headers=EXPECTED_HEADERS,
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
                                             headers=EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.output == self.EXPECTED_STDOUT_WHEN_WRONG_API_KEY_WAS_USED
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_request_and_print_proper_message_when_error_code_returned_without_json_data(self,
                                                                                                     post_patched):
        post_patched.return_value = MockResponse(status_code=500)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.output == "Failed to create resource\n"
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_tag_project(self, post_patched, get_patched, put_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON_WHEN_ALL_PARAMETERS_WERE_USED, 201)
        get_patched.return_value = MockResponse({}, 200, "fake content")
        put_patched.return_value = MockResponse(self.UPDATE_TAGS_RESPONSE_JSON_200, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_TAGS)

        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)

        put_patched.assert_called_once_with(
            self.TAGS_URL,
            headers=EXPECTED_HEADERS,
            json=self.TAGS_JSON,
            params=None,
            data=None,
        )

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        assert result.exit_code == 0


class TestDeleteProjects(object):
    URL = "https://api.paperspace.io/projects/some_project_id/deleteProject"
    BASIC_COMMAND = ["projects", "delete", "--id", "some_project_id"]
    EXPECTED_STDOUT = "Project deleted\n"

    BASIC_COMMAND_WITH_API_KEY = ["projects", "delete", "--id", "some_project_id", "--apiKey", "some_key"]
    COMMAND_WITH_OPTIONS_FILE = ["projects", "delete",
                                 "--id", "some_project_id",
                                 "--optionsFile", ]  # path added in test

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to delete resource: Invalid API token\n"

    RESPONSE_JSON_WHEN_PROJECT_IS_ALREADY_DELETED = {
        "error": {
            "name": "Error",
            "status": 400,
            "message": "Project \"some_project_id\" is already deleted.",
        },
    }
    EXPECTED_STDOUT_WHEN_PROJECT_IS_ALREADY_DELETED = \
        """Failed to delete resource: Project "some_project_id" is already deleted.\n"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_post_request_and_print_valid_message_when_delete_command_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=204)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        data=None,
                                        files=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_post_request_when_delete_was_used_with_api_key_option(self, post_patched):
        post_patched.return_value = MockResponse(status_code=204)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params=None,
                                        data=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, post_patched, projects_delete_config_path):
        post_patched.return_value = MockResponse(status_code=204)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [projects_delete_config_path]

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params=None,
                                        data=None,
                                        files=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_post_request_when_delete_was_used_with_wrong_api_key(self, post_patched):
        post_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params=None,
                                        data=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_post_request_when_the_project_is_already_deleted(self, post_patched):
        post_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_PROJECT_IS_ALREADY_DELETED,
                                                 status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params=None,
                                        data=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT_WHEN_PROJECT_IS_ALREADY_DELETED
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_error_message_when_project_was_not_found(self, post_patched):
        # TODO: add test later when the API is fixed - it responds with invalid message
        pass

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=None,
                                       data=None,
                                       files=None)
        assert result.output == "Failed to delete resource\n"
        assert result.exit_code == 0


class TestProjectsDetails(object):
    URL = "https://api.paperspace.io/projects/"
    EXPECTED_PARAMS = {
        "filter": """{"where":{"handle":"some_id"}}"""
    }
    BASIC_COMMAND = ["projects", "details", "--id", "some_id"]
    COMMAND_WITH_OPTIONS_FILE = ["projects", "details", "--id", "some_id", "--optionsFile", ]  # path added in test
    BASIC_COMMAND_WITH_API_KEY = ["projects", "details", "--id", "some_id", "--apiKey", "some_key"]

    EXPECTED_RESPONSE_JSON = example_responses.DETAILS_OF_PROJECT
    EXPECTED_STDOUT = """+-----------------+-----------+
| Name            | some_name |
+-----------------+-----------+
| ID              | some_id   |
| Repository name | None      |
| Repository url  | None      |
| Tags            |           |
+-----------------+-----------+
"""

    EXPECTED_RESPONSE_JSON_WITH_TAGS = example_responses.DETAILS_OF_PROJECT_WITH_TAGS
    EXPECTED_STDOUT_WITH_TAGS = """+-----------------+------------+
| Name            | some_name  |
+-----------------+------------+
| ID              | some_id    |
| Repository name | None       |
| Repository url  | None       |
| Tags            | tag1, tag2 |
+-----------------+------------+
"""

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to fetch data: Invalid API token\n"

    RESPONSE_JSON_WHEN_PROJECT_WAS_NOT_FOUND = {
        "data": [],
        "meta": {
            "where": {"handle": "some_id"},
            "totalItems": 0,
        },
        "tagFilter": [],
    }
    EXPECTED_STDOUT_WHEN_PROJECT_WAS_NOT_FOUND = "Project not found\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_and_print_table_when_projects_details_was_run(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.EXPECTED_PARAMS)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_and_print_table_when_projects_details_was_run_with_tags(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON_WITH_TAGS)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WITH_TAGS, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.EXPECTED_PARAMS)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_projects_details_was_used_with_api_key_option(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON_WITH_TAGS)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.EXPECTED_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WITH_TAGS
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, get_patched, projects_details_config_path):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON_WITH_TAGS)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [projects_details_config_path]

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT_WITH_TAGS, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.EXPECTED_PARAMS)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_projects_details_was_used_with_wrong_api_key(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.EXPECTED_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_error_message_when_project_was_not_found(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_PROJECT_WAS_NOT_FOUND)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.EXPECTED_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WHEN_PROJECT_WAS_NOT_FOUND
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.EXPECTED_PARAMS)
        assert result.output == "Failed to fetch data\n"
        assert result.exit_code == 0
