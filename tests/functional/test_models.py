import mock
from click.testing import CliRunner

import gradient.client
from gradient.cli import cli
from tests import example_responses, MockResponse


class TestModelsList(object):
    URL = "https://api.paperspace.io/mlModels/getModelList/"
    COMMAND = ["models", "list"]
    EXPECTED_HEADERS = gradient.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = gradient.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    COMMAND_WITH_FILTERING_BY_EXPERIMENT_ID = [
        "models", "list",
        "--experimentId", "some_experiment_id",
    ]
    EXPECTED_REQUEST_JSON_WITH_FILTERING = {"filter": {"where": {"and": [{"experimentId": "some_experiment_id"}]}}}

    COMMAND_WITH_API_KEY_PARAMETER_USED = ["models", "list", "--apiKey", "some_key"]

    EXPECTED_RESPONSE_JSON_WHEN_NO_MODELS_WERE_FOUND = {"modelList": [], "total": 1, "displayTotal": 0}

    EXPECTED_STDOUT = """+------+-----------------+------------+------------+---------------+
| Name | ID              | Model Type | Project ID | Experiment ID |
+------+-----------------+------------+------------+---------------+
| None | mosu30xm7q8vb0p | Tensorflow | prmr22ve0  | ehla1kvbwzaco |
+------+-----------------+------------+------------+---------------+
"""

    EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED = {"status": 401, "message": "No such API token"}

    @mock.patch("gradient.client.requests.get")
    def test_should_send_get_request_and_print_list_of_experiments(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.LIST_MODELS_RESPONSE_JSON, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params={"limit": -1})

        assert result.output == self.EXPECTED_STDOUT
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.client.requests.get")
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

    @mock.patch("gradient.client.requests.get")
    def test_should_send_get_request_and_print_list_of_models_filtered_experiment_id(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.LIST_MODELS_RESPONSE_JSON, 200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_FILTERING_BY_EXPERIMENT_ID)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=self.EXPECTED_REQUEST_JSON_WITH_FILTERING,
                                            params={"limit": -1})

        assert result.output == self.EXPECTED_STDOUT

    @mock.patch("gradient.client.requests.get")
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

    @mock.patch("gradient.client.requests.get")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED, 401)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params={"limit": -1})

        assert result.output == "No such API token\n"
