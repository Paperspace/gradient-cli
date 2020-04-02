import mock
from click.testing import CliRunner

from gradient.api_sdk.clients.http_client import default_headers
from gradient.cli import cli
from tests import MockResponse, example_responses

EXPECTED_HEADERS = default_headers.copy()
EXPECTED_HEADERS["ps_client_name"] = "gradient-cli"

EXPECTED_HEADERS_WITH_CHANGED_API_KEY = EXPECTED_HEADERS.copy()
EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"


class TestTensorboardsCreate(object):
    URL = "https://services.paperspace.io/tensorboards/v1/"
    COMMAND = [
        "tensorboards",
        "create",
        "--experiment", "some_experiment_id",
        "--experiment", "some_other_experiment_id",
    ]
    EXPECTED_REQUEST_JSON = {"experiments": ["some_experiment_id", "some_other_experiment_id"]}
    EXPECTED_RESPONSE_JSON = example_responses.TENSORBOARD_CREATE_RESPONSE_JSON
    EXPECTED_STDOUT = """Created new tensorboard with id: some_id\n"""

    COMMAND_WITH_API_KEY_CHANGED = [
        "tensorboards",
        "create",
        "--experiment", "some_experiment_id",
        "--experiment", "some_other_experiment_id",
        "--apiKey", "some_key",
    ]
    COMMAND_WITH_ALL_OPTIONS = [
        "tensorboards",
        "create",
        "--experiment", "some_experiment_id",
        "--experiment", "some_other_experiment_id",
        "--image", "some_image",
        "--username", "some_username",
        "--password", "some_password",
        "--apiKey", "some_key",
    ]

    EXPECTED_REQUEST_JSON_WITH_ALL_OPTIONS = {
        "experiments": [
            "some_experiment_id",
            "some_other_experiment_id",
        ],
        "image": "some_image",
        "username": "some_username",
        "password": "some_password"
    }
    COMMAND_WITH_OPTIONS_FILE_USED = ["tensorboards", "create", "--optionsFile", ]  # path added in test

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"title": "Invalid credentials provided"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to create resource: Invalid credentials provided\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_request_when_command_was_executed_with_required_options(self, post_patched):
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
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_request_with_changed_api_key_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_CHANGED)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             data=None,
                                             files=None,
                                             params=None)
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_request_when_command_was_executed_with_all_options(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_ALL_OPTIONS)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON_WITH_ALL_OPTIONS,
                                             data=None,
                                             files=None,
                                             params=None)
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, post_patched, tensorboards_create_config_path):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE_USED[:] + [tensorboards_create_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON_WITH_ALL_OPTIONS,
                                             data=None,
                                             files=None,
                                             params=None)
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"


class TestTensorboardsDetail(object):
    URL = "https://services.paperspace.io/tensorboards/v1/some_id/"
    COMMAND = [
        "tensorboards",
        "details",
        "--id", "some_id",
    ]
    EXPECTED_RESPONSE_JSON = example_responses.TENSORBOARD_DETAIL_RESPONSE_JSON
    EXPECTED_STDOUT = """+-------+--------------------------------------------------------+
| ID    | some_id                                                |
+-------+--------------------------------------------------------+
| Image | tensorflow/tensorflow:latest-py3                       |
| URL   | https://aws-testing.paperspace.io/tensorboard/some_id/ |
| State | Some State                                             |
+-------+--------------------------------------------------------+
+--------------------------+------------+
| Experiments ID           | State      |
+--------------------------+------------+
| some_experiment_id       | Some State |
| some_other_experiment_id | Some State |
+--------------------------+------------+
"""
    # TODO later change response to contain information about state: | State          | 1                             |

    COMMAND_WITH_API_KEY_CHANGED = [
        "tensorboards",
        "details",
        "--id", "some_id",
        "--apiKey", "some_key",
    ]
    COMMAND_WITH_OPTIONS_FILE_USED = ["tensorboards", "details", "--optionsFile", ]  # path added in test

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"title": "Invalid credentials provided"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to create resource: Invalid credentials provided\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_request_when_command_was_executed_with_required_options(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=None,
                                             params=None)
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_request_with_changed_api_key_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_CHANGED)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=None,
                                             params=None)
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, post_patched, tensorboards_details_config_path):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE_USED[:] + [tensorboards_details_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=None,
                                             params=None)
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"


class TestTensorboardsList(object):
    URL = "https://services.paperspace.io/tensorboards/v1/"
    COMMAND = ["tensorboards", "list"]
    EXPECTED_RESPONSE_JSON = example_responses.TENSORBOARD_LIST_RESPONSE_JSON
    EXPECTED_STDOUT = """+-----------------+----------------------------------------------------------------+------------+
| ID              | URL                                                            | STATE      |
+-----------------+----------------------------------------------------------------+------------+
| tbrs2kcjman4ly  | https://aws-testing.paperspace.io/tensorboard/tbrs2kcjman4ly/  | Some State |
| tbskzep6d9po04d | https://aws-testing.paperspace.io/tensorboard/tbskzep6d9po04d/ | Some State |
| tbsaq6hggzxcnet | https://aws-testing.paperspace.io/tensorboard/tbsaq6hggzxcnet/ | Some State |
| tbwuzalec7ik58  | https://aws-testing.paperspace.io/tensorboard/tbwuzalec7ik58/  | Some State |
+-----------------+----------------------------------------------------------------+------------+
"""

    COMMAND_WITH_API_KEY_CHANGED = ["tensorboards", "list", "--apiKey", "some_key"]
    COMMAND_WITH_OPTIONS_FILE_USED = ["tensorboards", "list", "--optionsFile", ]  # path added in test

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"title": "Invalid credentials provided"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to create resource: Invalid credentials provided\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_request_when_command_was_executed_with_required_options(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=None,
                                             params=None)
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_request_with_changed_api_key_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_CHANGED)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=None,
                                             params=None)
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, post_patched, tensorboards_details_config_path):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE_USED[:] + [tensorboards_details_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=None,
                                             params=None)
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"


class TestTensorboardsAddExperiment(object):
    URL = "https://services.paperspace.io/tensorboards/v1/some_id"
    COMMAND = ["tensorboards", "add-experiments", "--id", "some_id", "--experiment", "some_third_experiment_id"]

    EXPECTED_RESPONSE_JSON = example_responses.TENSORBOARD_UPDATE_RESPONSE_JSON
    EXPECTED_REQUEST_JSON = {"added_experiments": ["some_third_experiment_id"], "removed_experiments": []}
    EXPECTED_STDOUT = """+-------+--------------------------------------------------------+
| ID    | some_id                                                |
+-------+--------------------------------------------------------+
| Image | tensorflow/tensorflow:latest-py3                       |
| URL   | https://aws-testing.paperspace.io/tensorboard/some_id/ |
| State | Some State                                             |
+-------+--------------------------------------------------------+
+--------------------------+------------+
| Experiments ID           | State      |
+--------------------------+------------+
| some_experiment_id       | Some State |
| some_other_experiment_id | Some State |
| some_third_experiment_id | Some State |
+--------------------------+------------+
"""

    COMMAND_WITH_API_KEY_CHANGED = [
        "tensorboards", "add-experiments", "--id", "some_id",
        "--experiment", "some_third_experiment_id", "--apiKey", "some_key"
    ]

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"title": "Invalid credentials provided"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to update resource: Invalid credentials provided\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_send_valid_request_when_command_was_executed_with_required_options(self, put_patched):
        put_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        put_patched.assert_called_once_with(
            self.URL,
            headers=EXPECTED_HEADERS,
            json=self.EXPECTED_REQUEST_JSON,
            params=None,
            data=None,
        )
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_send_request_with_changed_api_key_when_api_key_option_was_used(self, put_patched):
        put_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=401)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_CHANGED)

        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN, result.exc_info
        put_patched.assert_called_once_with(
            self.URL,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
            json=self.EXPECTED_REQUEST_JSON,
            params=None,
            data=None,
        )


class TestTensorboardsRemoveExperiment(object):
    URL = "https://services.paperspace.io/tensorboards/v1/some_id"
    COMMAND = ["tensorboards", "remove-experiments", "--id", "some_id", "--experiment", "some_other_experiment_id"]

    EXPECTED_RESPONSE_JSON = example_responses.TENSORBOARD_UPDATE_REMOVE_RESPONSE_JSON
    EXPECTED_REQUEST_JSON = {"added_experiments": [], "removed_experiments": ["some_other_experiment_id"]}
    EXPECTED_STDOUT = """+-------+--------------------------------------------------------+
| ID    | some_id                                                |
+-------+--------------------------------------------------------+
| Image | tensorflow/tensorflow:latest-py3                       |
| URL   | https://aws-testing.paperspace.io/tensorboard/some_id/ |
| State | Some State                                             |
+-------+--------------------------------------------------------+
+--------------------+------------+
| Experiments ID     | State      |
+--------------------+------------+
| some_experiment_id | Some State |
+--------------------+------------+
"""

    COMMAND_WITH_API_KEY_CHANGED = [
        "tensorboards", "remove-experiments", "--id", "some_id",
        "--experiment", "some_other_experiment_id", "--apiKey", "some_key"
    ]

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"title": "Invalid credentials provided"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to update resource: Invalid credentials provided\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_send_valid_request_when_command_was_executed_with_required_options(self, put_patched):
        put_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        put_patched.assert_called_once_with(
            self.URL,
            headers=EXPECTED_HEADERS,
            json=self.EXPECTED_REQUEST_JSON,
            params=None,
            data=None,
        )
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_send_request_with_changed_api_key_when_api_key_option_was_used(self, put_patched):
        put_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=401)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_CHANGED)

        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN, result.exc_info
        put_patched.assert_called_once_with(
            self.URL,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
            json=self.EXPECTED_REQUEST_JSON,
            params=None,
            data=None,
        )


class TestTensorboardsDelete(object):
    URL = "https://services.paperspace.io/tensorboards/v1/some_id"
    COMMAND = ["tensorboards", "delete", "--id", "some_id"]

    EXPECTED_RESPONSE_JSON = example_responses.TENSORBOARD_DELETE_RESPONSE_JSON
    EXPECTED_REQUEST_JSON = {"added_experiments": [], "removed_experiments": ["some_other_experiment_id"]}
    EXPECTED_STDOUT = "Delete tensorboard (some_id) ended with success\n"

    COMMAND_WITH_API_KEY_CHANGED = [
        "tensorboards", "delete", "--id", "some_id", "--apiKey", "some_key"
    ]

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"title": "Invalid credentials provided"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to delete resource: Invalid credentials provided\n"

    RESPONSE_JSON_WITH_WRONG_ACCESS = {
        "error": "You don't have access to tensorboard some_id",
        "title": "401 Unauthorized"
    }
    EXPECTED_WRONG_ACCESS_RESPONSE = """Failed to delete resource: You don't have access to tensorboard some_id
401 Unauthorized
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.delete")
    def test_should_send_valid_request_when_command_was_executed_with_required_options(self, delete_patched):
        delete_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON, status_code=200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        delete_patched.assert_called_once_with(
            self.URL,
            headers=EXPECTED_HEADERS,
            json=None,
            params=None
        )
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.delete")
    def test_should_send_request_with_changed_api_key_when_api_key_option_was_used(self, delete_patched):
        delete_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=401)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_CHANGED)

        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN, result.exc_info
        delete_patched.assert_called_once_with(
            self.URL,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
            json=None,
            params=None
        )

    @mock.patch("gradient.api_sdk.clients.http_client.requests.delete")
    def test_should_send_request_to_remove_tensorboard_without_proper_access(self, delete_patched):
        delete_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_ACCESS, status_code=401)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_WRONG_ACCESS_RESPONSE, result.exc_info
        delete_patched.assert_called_once_with(
            self.URL,
            headers=EXPECTED_HEADERS,
            json=None,
            params=None
        )
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"
