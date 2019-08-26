import mock
from click.testing import CliRunner

import gradient.api_sdk.clients.http_client
from gradient.cli import cli
from tests import example_responses, MockResponse


class TestModelsList(object):
    URL = "https://api.paperspace.io/mlModels/getModelList/"
    COMMAND = ["models", "list"]
    EXPECTED_HEADERS = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    COMMAND_WITH_FILTERING_BY_EXPERIMENT_ID = [
        "models", "list",
        "--experimentId", "some_experiment_id",
        "--projectId", "some_project_id",
    ]
    EXPECTED_REQUEST_JSON_WITH_FILTERING = {"filter": {"where": {"and": [{"projectId": "some_project_id",
                                                                          "experimentId": "some_experiment_id"}]}}}

    COMMAND_WITH_API_KEY_PARAMETER_USED = ["models", "list", "--apiKey", "some_key"]
    COMMAND_WITH_OPTIONS_FILE = ["models", "list", "--optionsFile", ]  # path added in test

    EXPECTED_RESPONSE_JSON_WHEN_NO_MODELS_WERE_FOUND = {"modelList": [], "total": 1, "displayTotal": 0}

    EXPECTED_STDOUT = """+------+-----------------+------------+------------+---------------+
| Name | ID              | Model Type | Project ID | Experiment ID |
+------+-----------------+------------+------------+---------------+
| None | mosu30xm7q8vb0p | Tensorflow | prmr22ve0  | ehla1kvbwzaco |
+------+-----------------+------------+------------+---------------+
"""

    EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED = {"status": 401, "message": "No such API token"}

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_list_of_experiments(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.LIST_MODELS_RESPONSE_JSON, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params={"limit": -1})

        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_replate_api_key_in_headers_when_api_key_parameter_was_used(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.LIST_MODELS_RESPONSE_JSON, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_PARAMETER_USED)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params={"limit": -1})

        assert result.output == self.EXPECTED_STDOUT
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, get_patched, models_list_config_path):
        get_patched.return_value = MockResponse(example_responses.LIST_MODELS_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [models_list_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=self.EXPECTED_REQUEST_JSON_WITH_FILTERING,
                                            params={"limit": -1})

        assert result.output == self.EXPECTED_STDOUT
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_list_of_models_filtered_experiment_id(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.LIST_MODELS_RESPONSE_JSON, 200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_FILTERING_BY_EXPERIMENT_ID)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=self.EXPECTED_REQUEST_JSON_WITH_FILTERING,
                                            params={"limit": -1})

        assert result.output == self.EXPECTED_STDOUT

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_proper_message_when_no_models_were_found(
            self, get_patched):
        get_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON_WHEN_NO_MODELS_WERE_FOUND, 200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params={"limit": -1})

        assert result.output == "No data found\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED, 401)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params={"limit": -1})

        assert result.output == "Failed to fetch data: No such API token\n"
