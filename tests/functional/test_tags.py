import mock
import pytest
from click.testing import CliRunner

from gradient.api_sdk.clients.http_client import default_headers
from gradient.cli import cli
from tests import example_responses, MockResponse

EXPECTED_HEADERS = default_headers.copy()
EXPECTED_HEADERS["ps_client_name"] = "gradient-cli"

EXPECTED_HEADERS_WITH_CHANGED_API_KEY = EXPECTED_HEADERS.copy()
EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"


class TestEntityAddTags(object):
    URL = "https://api.paperspace.io/entityTags/updateTags"

    COMMAND = [
        "tags", "add",
        "--tag", "test0",
        "--tag", "test1",
        "--tags", "test2,test3",
        "--id", "some_id",
    ]
    COMMAND_WITH_OPTIONS_FILE = ["tags", "add",
                                 "--optionsFile", ]  # path added in test

    TAGS_JSON = {
        "entity": "",
        "entityId": "some_id",
        "tags": ["test0", "test1", "test2", "test3"]
    }
    UPDATE_TAGS_RESPONSE_JSON_200 = example_responses.UPDATE_TAGS_RESPONSE
    EXPECTED_STDOUT = "Tags added to %s\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @pytest.mark.parametrize(
        "entity_command, entity, result_entity",
        [
            # ("deployments", "deployment", "deployment"),
            ("experiments", "experiment", "experiment"),
            ("experiments hyperparameters", "experiment", "hyperparameter"),
            ("jobs", "job", "job"),
            ("machines", "machine", "machine"),
            ("models", "mlModel", "ml model"),
            ("notebooks", "notebook", "notebook"),
            ("projects", "project", "project"),
        ]
    )
    def test_should_send_proper_data_and_success(self, get_patched, put_patched, entity_command, entity, result_entity):
        entity_command = entity_command.split(" ")
        command = entity_command + self.COMMAND

        tags_json = self.TAGS_JSON.copy()
        tags_json["entity"] = entity
        expected_result = self.EXPECTED_STDOUT % result_entity

        get_patched.return_value = MockResponse({}, 200, "fake content")
        put_patched.return_value = MockResponse(
            self.UPDATE_TAGS_RESPONSE_JSON_200, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == expected_result, result.exc_info
        put_patched.assert_called_once_with(
            self.URL,
            headers=EXPECTED_HEADERS,
            json=tags_json,
            params=None,
            data=None,
        )

        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @pytest.mark.parametrize(
        "entity_command, entity, result_entity",
        [
            # ("deployments", "deployment", "deployment"),
            ("experiments", "experiment", "experiment"),
            ("experiments hyperparameters", "experiment", "hyperparameter"),
            ("jobs", "job", "job"),
            ("machines", "machine", "machine"),
            ("models", "mlModel", "ml model"),
            ("notebooks", "notebook", "notebook"),
            ("projects", "project", "project"),
        ]
    )
    def test_should_read_options_from_yaml_file(
            self, get_patched, put_patched, entity_tags_add_config_path, entity_command, entity, result_entity
    ):
        get_patched.return_value = MockResponse({}, 200, "fake content")
        put_patched.return_value = MockResponse(
            self.UPDATE_TAGS_RESPONSE_JSON_200, 200, "fake content")

        entity_command = entity_command.split(" ")
        command = entity_command + self.COMMAND_WITH_OPTIONS_FILE + \
            [entity_tags_add_config_path]

        tags_json = self.TAGS_JSON.copy()
        tags_json["entity"] = entity
        expected_result = self.EXPECTED_STDOUT % result_entity

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        put_patched.assert_called_once_with(
            self.URL,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
            json=tags_json,
            params=None,
            data=None,
        )

        assert result.output == expected_result, result.exc_info
        assert result.exit_code == 0


class TestEntityRemoveTags(object):
    URL = "https://api.paperspace.io/entityTags/updateTags"

    COMMAND = [
        "tags", "remove",
        "--tag", "test0",
        "--tags", "test2",
        "--id", "some_id",
    ]
    COMMAND_WITH_OPTIONS_FILE = ["tags", "remove",
                                 "--optionsFile", ]  # path added in test

    GET_TAGS_MOCK_RESPONSE = example_responses.GET_TAGS_RESPONSE

    TAGS_JSON = {
        "entity": "",
        "entityId": "some_id",
        "tags": ["test1", "test3"]
    }
    UPDATE_TAGS_RESPONSE_JSON_200 = example_responses.UPDATE_TAGS_RESPONSE
    EXPECTED_STDOUT = "Tags removed from %s\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @pytest.mark.parametrize(
        "entity_command, entity, result_entity",
        [
            # ("deployments", "deployment", "deployment"),
            ("experiments", "experiment", "experiment"),
            ("experiments hyperparameters", "experiment", "hyperparameter"),
            ("jobs", "job", "job"),
            ("machines", "machine", "machine"),
            ("models", "mlModel", "ml model"),
            ("notebooks", "notebook", "notebook"),
            ("projects", "project", "project"),
        ]
    )
    def test_should_send_proper_data_and_success(self, get_patched, put_patched, entity_command, entity, result_entity):
        entity_command = entity_command.split(" ")
        command = entity_command + self.COMMAND

        tags_json = self.TAGS_JSON.copy()
        tags_json["entity"] = entity
        expected_result = self.EXPECTED_STDOUT % result_entity

        get_patched.return_value = MockResponse(
            self.GET_TAGS_MOCK_RESPONSE, 200, "fake content")
        put_patched.return_value = MockResponse(
            self.UPDATE_TAGS_RESPONSE_JSON_200, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == expected_result, result.exc_info
        put_patched.assert_called_once_with(
            self.URL,
            headers=EXPECTED_HEADERS,
            json=tags_json,
            params=None,
            data=None,
        )

        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @pytest.mark.parametrize(
        "entity_command, entity, result_entity",
        [
            # ("deployments", "deployment", "deployment"),
            ("experiments", "experiment", "experiment"),
            ("experiments hyperparameters", "experiment", "hyperparameter"),
            ("jobs", "job", "job"),
            ("machines", "machine", "machine"),
            ("models", "mlModel", "ml model"),
            ("notebooks", "notebook", "notebook"),
            ("projects", "project", "project"),
        ]
    )
    def test_should_read_options_from_yaml_file(
            self, get_patched, put_patched, entity_tags_remove_config_path, entity_command, entity, result_entity
    ):
        get_patched.return_value = MockResponse(
            self.GET_TAGS_MOCK_RESPONSE, 200, "fake content")
        put_patched.return_value = MockResponse(
            self.UPDATE_TAGS_RESPONSE_JSON_200, 200, "fake content")

        entity_command = entity_command.split(" ")
        command = entity_command + self.COMMAND_WITH_OPTIONS_FILE + \
            [entity_tags_remove_config_path]

        tags_json = self.TAGS_JSON.copy()
        tags_json["entity"] = entity
        expected_result = self.EXPECTED_STDOUT % result_entity

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == expected_result, result.exc_info
        put_patched.assert_called_once_with(
            self.URL,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
            json=tags_json,
            params=None,
            data=None,
        )

        assert result.exit_code == 0
