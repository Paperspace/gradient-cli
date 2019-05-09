import mock
from click.testing import CliRunner

import paperspace
from paperspace.cli import cli
from paperspace.client import default_headers
from tests import example_responses, MockResponse


class TestListProjects(object):
    URL = "https://api.paperspace.io/projects/"
    EXPECTED_HEADERS = default_headers.copy()
    BASIC_COMMAND = ["projects", "list"]
    # TODO: change to `REQUEST_JSON = None` or whatever works when PS_API is fixed
    REQUEST_JSON = {'teamId': 666}
    EXPECTED_RESPONSE_JSON = example_responses.LIST_PROJECTS_RESPONSE
    EXPECTED_STDOUT = """+-----------+-------------------+------------+--------------------------+
| ID        | Name              | Repository | Created                  |
+-----------+-------------------+------------+--------------------------+
| prq70zy79 | test_project      | None       | 2019-03-18T13:24:46.666Z |
| prmr22ve0 | keton             | None       | 2019-03-25T14:50:43.202Z |
| przhbct98 | paperspace-python | None       | 2019-04-04T15:12:34.229Z |
+-----------+-------------------+------------+--------------------------+
"""

    BASIC_COMMAND_WITH_API_KEY = ["projects", "list", "--apiKey", "some_key"]
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Invalid API token\n"

    RESPONSE_JSON_WHEN_NO_PROJECTS_WERE_FOUND = {"data": [], "meta": {"totalItems": 0}}
    EXPECTED_STDOUT_WHEN_NO_PROJECTS_WERE_FOUND = "No data found\n"

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_valid_post_request_and_print_table_when_projects_list_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.REQUEST_JSON,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_valid_post_request_when_projects_list_was_used_with_api_key_option(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=self.REQUEST_JSON,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_valid_post_request_when_projects_list_was_used_with_wrong_api_key(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=self.REQUEST_JSON,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_print_error_message_when_no_project_was_not_found(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_NO_PROJECTS_WERE_FOUND,
                                                status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.REQUEST_JSON,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT_WHEN_NO_PROJECTS_WERE_FOUND
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.REQUEST_JSON,
                                       params=None)
        assert result.output == "Error while parsing response data: No JSON\n"
        assert result.exit_code == 0
