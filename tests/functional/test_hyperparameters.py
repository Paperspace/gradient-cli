import mock
from click.testing import CliRunner

from gradient.api_sdk import constants
from gradient.api_sdk.clients.http_client import default_headers
from gradient.cli import cli
from tests import MockResponse, example_responses

EXPECTED_HEADERS = default_headers.copy()
EXPECTED_HEADERS["ps_client_name"] = "gradient-cli"

EXPECTED_HEADERS_WITH_CHANGED_API_KEY = EXPECTED_HEADERS.copy()
EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"


class TestCreateHyperparameters(object):
    URL_V2 = "https://services.paperspace.io/experiments/v2/hyperopt/"
    TAGS_URL = "https://api.paperspace.io/entityTags/updateTags"
    COMMAND = [
        "experiments", "hyperparameters", "create",
        "--name", "some_name",
        "--tuningCommand", "some command",
        "--workerContainer", "some_container",
        "--workerMachineType", "k80",
        "--workerCommand", "some worker command",
        "--workerCount", "1",
        "--projectId", "some_project_id",
    ]
    COMMAND_WITH_TAGS = [
        "experiments", "hyperparameters", "create",
        "--name", "some_name",
        "--tuningCommand", "some command",
        "--workerContainer", "some_container",
        "--workerMachineType", "k80",
        "--workerCommand", "some worker command",
        "--workerCount", "1",
        "--projectId", "some_project_id",
        "--tag", "test0",
        "--tag", "test1",
        "--tags", "test2,test3",
    ]
    EXPECTED_REQUEST_JSON = {
        "workerContainer": "some_container",
        "workerMachineType": "k80",
        "name": "some_name",
        "tuningCommand": "c29tZSBjb21tYW5k",
        "workerCount": 1,
        "workerCommand": "c29tZSB3b3JrZXIgY29tbWFuZA==",
        "experimentTypeId": constants.ExperimentType.HYPERPARAMETER_TUNING,
        "projectHandle": "some_project_id",
    }
    TAGS_JSON = {
        "entity": "experiment",
        "entityId": "eshgvasywz9k1w",
        "tags": ["test0", "test1", "test2", "test3"]
    }
    UPDATE_TAGS_RESPONSE_JSON_200 = example_responses.UPDATE_TAGS_RESPONSE

    COMMAND_WHEN_ALL_PARAMETERS_WERE_USED = [
        "experiments", "hyperparameters", "create",
        "--name", "some_name",
        "--tuningCommand", "some command",
        "--workerContainer", "some_worker_container",
        "--workerMachineType", "k80",
        "--workerCommand", "some worker command",
        "--workerCount", "666",
        "--projectId", "some_project_id",
        "--workerRegistryUsername", "some_registry_username",
        "--workerRegistryPassword", "some_registry_password",
        "--workerContainerUser", "some_worker_container_user",
        "--hyperparameterServerRegistryUsername", "some_hyperparameter_registry_username",
        "--hyperparameterServerRegistryPassword", "some_hyperparameter_registry_password",
        "--hyperparameterServerContainer", "some_hyperparameter_container",
        "--hyperparameterServerContainerUser", "some_hyperparameter_container_user",
        "--hyperparameterServerMachineType", "some_hyperparameter_server_machine",
        "--modelPath", "some_model_path",
        "--modelType", "some_model_type",
        "--ignoreFiles", "file1,file2",
        "--isPreemptible",
        "--artifactDirectory", "some_artifact_directory",
        "--clusterId", "some_cluster_id",
        "--experimentEnv", "{\"key\":\"val\"}",
        "--ignoreFiles", "file2",
        "--ports", "8080,9000:9999",
        "--workerDockerfilePath", "some_docker_path",
        "--workerUseDockerfile",
        "--workingDirectory", "some_working_directory",
        "--workspace", "s3://some-path",
    ]
    EXPECTED_REQUEST_JSON_WHEN_ALL_PARAMETERS_WERE_USED = {
        "workerContainer": "some_worker_container",
        "workerMachineType": "k80",
        "name": "some_name",
        "tuningCommand": "c29tZSBjb21tYW5k",
        "workerCount": 666,
        "workerCommand": "c29tZSB3b3JrZXIgY29tbWFuZA==",
        "workerRegistryUsername": "some_registry_username",
        "workerRegistryPassword": "some_registry_password",
        "workerContainerUser": "some_worker_container_user",
        "projectHandle": "some_project_id",
        "hyperparameterServerRegistryUsername": "some_hyperparameter_registry_username",
        "hyperparameterServerRegistryPassword": "some_hyperparameter_registry_password",
        "hyperparameterServerContainer": "some_hyperparameter_container",
        "hyperparameterServerContainerUser": "some_hyperparameter_container_user",
        "hyperparameterServerMachineType": "some_hyperparameter_server_machine",
        "experimentTypeId": constants.ExperimentType.HYPERPARAMETER_TUNING,
        "modelPath": "some_model_path",
        "modelType": "some_model_type",
        "isPreemptible": True,
        "dockerfilePath": "some_docker_path",
        "artifactDirectory": "some_artifact_directory",
        "clusterId": "some_cluster_id",
        "experimentEnv": {"key": "val"},
        "ports": "8080,9000:9999",
        "useDockerfile": True,
        "workingDirectory": "some_working_directory",
        "workspaceUrl": "s3://some-path",
    }
    COMMAND_WITH_OPTIONS_FILE = ["experiments", "hyperparameters", "create", "--optionsFile", ]  # path added in test

    EXPECTED_RESPONSE = {"handle": "eshgvasywz9k1w", "message": "success"}
    EXPECTED_STDOUT = "Hyperparameter tuning job created with ID: eshgvasywz9k1w\n" \
                      "https://console.paperspace.com/projects/some_project_id/experiments/eshgvasywz9k1w\n"

    EXPECTED_RESPONSE_JSON_WITH_ERROR = {
        "details": {
            "projectHandle": ["Missing data for required field."],
        },
        "error": "Experiment data error",
    }
    EXPECTED_STDOUT_WHEN_ERROR_RECEIVED = "Failed to create resource: projectHandle: Missing data for required field." \
                                          "\nExperiment data error\n"

    COMMAND_WITH_API_KEY_PARAMETER_USED = [
        "experiments", "hyperparameters", "create",
        "--name", "some_name",
        "--tuningCommand", "some command",
        "--workerContainer", "some_container",
        "--workerMachineType", "k80",
        "--workerCommand", "some worker command",
        "--workerCount", "1",
        "--projectId", "some_project_id",
        "--apiKey", "some_key",
    ]
    EXPECTED_REQUEST_JSON_WHEN_API_KEY_PARAMETERS_WAS_USED = {
        "workerContainer": "some_container",
        "workerMachineType": "k80",
        "name": "some_name",
        "tuningCommand": "some command",
        "workerCount": 1,
        "workerCommand": "some worker command",
        "projectHandle": "pr4yxj956",
        "experimentTypeId": constants.ExperimentType.HYPERPARAMETER_TUNING,
    }

    EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED = {"details": "Incorrect API Key provided", "error": "Forbidden"}
    EXPECTED_STDOUT_WHEN_WRONG_API_KEY_WAS_USED = "Failed to create resource: Incorrect API Key provided\nForbidden\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_get_request_and_print_proper_message_when_create_command_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE, 201)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)

        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_get_request_and_print_proper_message_when_create_command_was_used_with_all_options(self,
                                                                                                            post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE, 201)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WHEN_ALL_PARAMETERS_WERE_USED)

        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON_WHEN_ALL_PARAMETERS_WERE_USED,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.output == self.EXPECTED_STDOUT
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_replace_api_key_in_headers_when_api_key_parameter_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE, 201)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_PARAMETER_USED)

        assert result.output == self.EXPECTED_STDOUT
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_proper_message_when_error_message_received(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON_WITH_ERROR, 400)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL_V2,
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

        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.output == self.EXPECTED_STDOUT_WHEN_WRONG_API_KEY_WAS_USED
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, post_patched, hyperparameters_create_config_path):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [hyperparameters_create_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON_WHEN_ALL_PARAMETERS_WERE_USED,
                                             params=None,
                                             files=None,
                                             data=None)

        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_request_and_print_proper_message_when_error_code_returned_without_json_data(self,
                                                                                                     post_patched):
        post_patched.return_value = MockResponse(status_code=500)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL_V2,
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
    def test_should_send_proper_data_and_tag_hyperopt_experiment(self, post_patched, get_patched, put_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE)
        get_patched.return_value = MockResponse({}, )
        put_patched.return_value = MockResponse(self.UPDATE_TAGS_RESPONSE_JSON_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_TAGS)

        post_patched.assert_called_once_with(self.URL_V2,
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


class TestCreateAndStartHyperparameters(object):
    URL_V2 = "https://services.paperspace.io/experiments/v2/hyperopt/create_and_start/"
    COMMAND = [
        "experiments", "hyperparameters", "run",
        "--name", "some_name",
        "--tuningCommand", "some command",
        "--workerContainer", "some_container",
        "--workerMachineType", "k80",
        "--workerCommand", "some worker command",
        "--workerCount", "1",
        "--projectId", "some_project_id",
    ]
    EXPECTED_REQUEST_JSON = {
        "workerContainer": "some_container",
        "workerMachineType": "k80",
        "name": "some_name",
        "tuningCommand": "c29tZSBjb21tYW5k",
        "workerCount": 1,
        "workerCommand": "c29tZSB3b3JrZXIgY29tbWFuZA==",
        "projectHandle": "some_project_id",
        "experimentTypeId": constants.ExperimentType.HYPERPARAMETER_TUNING,
    }

    COMMAND_WHEN_ALL_PARAMETERS_WERE_USED = [
        "experiments", "hyperparameters", "run",
        "--name", "some_name",
        "--tuningCommand", "some command",
        "--workerContainer", "some_worker_container",
        "--workerMachineType", "k80",
        "--workerCommand", "some worker command",
        "--workerCount", "666",
        "--projectId", "some_project_id",
        "--workerRegistryUsername", "some_registry_username",
        "--workerRegistryPassword", "some_registry_password",
        "--workerContainerUser", "some_worker_container_user",
        "--hyperparameterServerRegistryUsername", "some_hyperparameter_registry_username",
        "--hyperparameterServerRegistryPassword", "some_hyperparameter_registry_password",
        "--hyperparameterServerContainer", "some_hyperparameter_container",
        "--hyperparameterServerContainerUser", "some_hyperparameter_container_user",
        "--hyperparameterServerMachineType", "some_hyperparameter_server_machine",
        "--modelPath", "some_model_path",
        "--modelType", "some_model_type",
        "--ignoreFiles", "file1,file2",
        "--isPreemptible",
        "--artifactDirectory", "some_artifact_directory",
        "--clusterId", "some_cluster_id",
        "--experimentEnv", "{\"key\":\"val\"}",
        "--ignoreFiles", "file2",
        "--ports", "8080,9000:9999",
        "--workerDockerfilePath", "some_docker_path",
        "--workerUseDockerfile",
        "--workingDirectory", "some_working_directory",
        "--workspace", "s3://some-path",
    ]
    EXPECTED_REQUEST_JSON_WHEN_ALL_PARAMETERS_WERE_USED = {
        "workerContainer": "some_worker_container",
        "workerMachineType": "k80",
        "name": "some_name",
        "tuningCommand": "c29tZSBjb21tYW5k",
        "workerCount": 666,
        "workerCommand": "c29tZSB3b3JrZXIgY29tbWFuZA==",
        "workerRegistryUsername": "some_registry_username",
        "workerRegistryPassword": "some_registry_password",
        "workerContainerUser": "some_worker_container_user",
        "projectHandle": "some_project_id",
        "hyperparameterServerRegistryUsername": "some_hyperparameter_registry_username",
        "hyperparameterServerRegistryPassword": "some_hyperparameter_registry_password",
        "hyperparameterServerContainer": "some_hyperparameter_container",
        "hyperparameterServerContainerUser": "some_hyperparameter_container_user",
        "hyperparameterServerMachineType": "some_hyperparameter_server_machine",
        "experimentTypeId": constants.ExperimentType.HYPERPARAMETER_TUNING,
        "modelPath": "some_model_path",
        "modelType": "some_model_type",
        "isPreemptible": True,
        "dockerfilePath": "some_docker_path",
        "artifactDirectory": "some_artifact_directory",
        "clusterId": "some_cluster_id",
        "experimentEnv": {"key": "val"},
        "ports": "8080,9000:9999",
        "useDockerfile": True,
        "workingDirectory": "some_working_directory",
        "workspaceUrl": "s3://some-path",
    }
    COMMAND_WITH_OPTIONS_FILE = ["experiments", "hyperparameters", "run", "--optionsFile", ]  # path added in test

    EXPECTED_RESPONSE = {"handle": "eshgvasywz9k1w", "message": "success"}
    EXPECTED_STDOUT = "Hyperparameter tuning job created and started with ID: eshgvasywz9k1w\n" \
                      "https://console.paperspace.com/projects/some_project_id/experiments/eshgvasywz9k1w\n"

    EXPECTED_RESPONSE_JSON_WITH_ERROR = {
        "details": {
            "projectHandle": ["Missing data for required field."],
        },
        "error": "Experiment data error",
    }
    EXPECTED_STDOUT_WHEN_ERROR_RECEIVED = "Failed to create resource: " \
                                          "projectHandle: Missing data for required field.\nExperiment data error\n"

    COMMAND_WITH_API_KEY_PARAMETER_USED = [
        "experiments", "hyperparameters", "run",
        "--name", "some_name",
        "--tuningCommand", "some command",
        "--workerContainer", "some_container",
        "--workerMachineType", "k80",
        "--workerCommand", "some worker command",
        "--workerCount", "1",
        "--projectId", "some_project_id",
        "--apiKey", "some_key",
    ]
    EXPECTED_REQUEST_JSON_WHEN_API_KEY_PARAMETERS_WAS_USED = {
        "workerContainer": "some_container",
        "workerMachineType": "k80",
        "name": "some_name",
        "tuningCommand": "some command",
        "workerCount": 1,
        "workerCommand": "some worker command",
        "projectHandle": "pr4yxj956",
        "experimentTypeId": constants.ExperimentType.HYPERPARAMETER_TUNING,
    }

    EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED = {"details": "Incorrect API Key provided", "error": "Forbidden"}
    EXPECTED_STDOUT_WHEN_WRONG_API_KEY_WAS_USED = "Failed to create resource: Incorrect API Key provided\nForbidden\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_get_request_and_print_proper_message_when_create_command_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE, 201)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)

        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_get_request_and_print_proper_message_when_create_command_was_used_with_all_options(self,
                                                                                                            post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE, 201)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WHEN_ALL_PARAMETERS_WERE_USED)

        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON_WHEN_ALL_PARAMETERS_WERE_USED,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.output == self.EXPECTED_STDOUT
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_replace_api_key_in_headers_when_api_key_parameter_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE, 201)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_PARAMETER_USED)

        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.output == self.EXPECTED_STDOUT
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_proper_message_when_error_message_received(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON_WITH_ERROR, 400)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL_V2,
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

        post_patched.assert_called_once_with(self.URL_V2,
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

        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.output == "Failed to create resource\n"
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, post_patched, hyperparameters_create_config_path):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [hyperparameters_create_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON_WHEN_ALL_PARAMETERS_WERE_USED,
                                             params=None,
                                             files=None,
                                             data=None)
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"


class TestStartHyperparameters(object):
    URL_V2 = "https://services.paperspace.io/experiments/v2/hyperopt/some_id/start/"
    COMMAND = [
        "experiments", "hyperparameters", "start",
        "--id", "some_id",
    ]

    COMMAND_WITH_OPTIONS_FILE = ["experiments", "hyperparameters", "start", "--optionsFile", ]  # path added in test

    EXPECTED_RESPONSE = {"message": "success"}
    EXPECTED_STDOUT = "Hyperparameter tuning started\n"

    EXPECTED_RESPONSE_JSON_WITH_ERROR = {"error": "Could not find cluster meeting requirements"}
    EXPECTED_STDOUT_WHEN_ERROR_RECEIVED = "Failed to start hyperparameter tuning job: Could not find cluster meeting requirements\n"

    COMMAND_WITH_API_KEY_PARAMETER_USED = [
        "experiments", "hyperparameters", "start",
        "--id", "some_id",
        "--apiKey", "some_key",
    ]
    EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED = {"details": "Incorrect API Key provided", "error": "Forbidden"}
    EXPECTED_STDOUT_WHEN_WRONG_API_KEY_WAS_USED = "Failed to start hyperparameter tuning job: Incorrect API Key provided\nForbidden\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_send_get_request_and_print_proper_message_when_start_command_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE, 201)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS,
                                             json=None,
                                             params=None,
                                             data=None,
                                             )
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_replace_api_key_in_headers_when_api_key_parameter_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE, 201)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_PARAMETER_USED)

        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=None,
                                             params=None,
                                             data=None,
                                             )

        assert result.output == self.EXPECTED_STDOUT
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_read_options_from_yaml_file(self, post_patched, hyperparameters_start_config_path):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE, 201)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [hyperparameters_start_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=None,
                                             params=None,
                                             data=None,
                                             )

        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_print_proper_message_when_error_message_received(self, put_patched):
        put_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON_WITH_ERROR, 400)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        put_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None,
                                            data=None,
                                            )

        assert result.output == self.EXPECTED_STDOUT_WHEN_ERROR_RECEIVED

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, put_patched):
        put_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED, 403)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        put_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None,
                                            data=None,
                                            )

        assert result.output == self.EXPECTED_STDOUT_WHEN_WRONG_API_KEY_WAS_USED
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_send_request_and_print_proper_message_when_error_code_returned_without_json_data(self, put_patched):
        put_patched.return_value = MockResponse(status_code=500)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        put_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None,
                                            data=None,
                                            )

        assert result.output == "Failed to start hyperparameter tuning job\n"
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"


class TestHyperparametersList(object):
    URL_V2 = "https://services.paperspace.io/experiments/v2/hyperopt/"
    COMMAND = ["experiments", "hyperparameters", "list"]
    COMMAND_WITH_OPTIONS_FILE = ["experiments", "hyperparameters", "list", "--optionsFile", ]  # path added in test
    EXPECTED_REQUEST_PARAMS = {"limit": -1}

    COMMAND_WITH_API_KEY_PARAMETER_USED = ["experiments", "hyperparameters", "list", "--apiKey", "some_key"]

    EXPECTED_RESPONSE_JSON_WHEN_NO_OBJECTS_WERE_FOUND = {
        "data": [],
        "message": "success",
        "meta": {
            "filter": [],
            "limit": -1,
            "offset": 0,
            "totalItems": 0,
        },
    }

    EXPECTED_STDOUT = """+-----------+----------------+------------+
| Name      | ID             | Project ID |
+-----------+----------------+------------+
| some_name | es3dn6fu16r4kk | pr4yxj956  |
| some_name | eshlqek7wzvrxa | pr4yxj956  |
| some_name | esdwnui5qsk8qm | pr4yxj956  |
| some_name | eshz1z9k37w4nm | pr4yxj956  |
+-----------+----------------+------------+
"""

    EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED = {"status": 401, "message": "No such API token"}

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_list_of_hyperparameters(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.LIST_HYPERPARAMETERS_RESPONSE_JSON, 200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=self.EXPECTED_REQUEST_PARAMS)
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_replace_api_key_in_headers_when_api_key_parameter_was_used(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.LIST_HYPERPARAMETERS_RESPONSE_JSON, 200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_PARAMETER_USED)

        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=self.EXPECTED_REQUEST_PARAMS)

        assert result.output == self.EXPECTED_STDOUT
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml(self, get_patched, hyperparameters_list_config_path):
        get_patched.return_value = MockResponse(example_responses.LIST_HYPERPARAMETERS_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [hyperparameters_list_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=self.EXPECTED_REQUEST_PARAMS)

        assert result.output == self.EXPECTED_STDOUT
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_proper_message_when_no_objects_were_found(
            self, get_patched):
        get_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON_WHEN_NO_OBJECTS_WERE_FOUND, 200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=self.EXPECTED_REQUEST_PARAMS)

        assert result.output == "No data found\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED, 401)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=self.EXPECTED_REQUEST_PARAMS)

        assert result.output == "Failed to fetch data: No such API token\n"


class TestHyperparametersDetails(object):
    URL_V2 = "https://services.paperspace.io/experiments/v2/hyperopt/some_id/"
    COMMAND = ["experiments", "hyperparameters", "details", "--id", "some_id"]

    COMMAND_WITH_OPTIONS_FILE = ["experiments", "hyperparameters", "details", "--optionsFile", ]  # path added in test
    COMMAND_WITH_API_KEY_PARAMETER_USED = [
        "experiments", "hyperparameters", "details",
        "--id", "some_id",
        "--apiKey", "some_key",
    ]

    EXPECTED_RESPONSE_JSON_WHEN_NO_OBJECT_WAS_NOT_FOUND = {"error": "Hyperopt not found"}

    EXPECTED_STDOUT = """+-----------------------+---------------------+
| ID                    | ess6t3fjs2hb1g      |
+-----------------------+---------------------+
| Name                  | some_name           |
| Ports                 | 5000                |
| Project ID            | pr4yxj956           |
| Tuning command        | some command        |
| Worker command        | some worker command |
| Worker container      | some_container      |
| Worker count          | 1                   |
| Worker machine type   | k80                 |
| Worker use dockerfile | False               |
| Workspace URL         | none                |
+-----------------------+---------------------+
"""

    EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED = {"status": 401, "message": "No such API token"}

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_details_of_hyperparameters_job(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.HYPERPARAMETERS_DETAILS_RESPONSE_JSON, 200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_replace_api_key_in_headers_when_api_key_parameter_was_used(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.HYPERPARAMETERS_DETAILS_RESPONSE_JSON, 200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_PARAMETER_USED)

        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=None)

        assert result.output == self.EXPECTED_STDOUT
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(
            self, get_patched, hyperparameters_details_config_path):
        get_patched.return_value = MockResponse(example_responses.HYPERPARAMETERS_DETAILS_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [hyperparameters_details_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=None)
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_proper_message_when_no_objects_were_found(self, get_patched):
        get_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON_WHEN_NO_OBJECT_WAS_NOT_FOUND, 404)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

        assert result.output == "Failed to fetch data: Hyperopt not found\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED, 401)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

        assert result.output == "Failed to fetch data: No such API token\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_proper_message_when_got_error_response_without_data(self, get_patched):
        get_patched.return_value = MockResponse(status_code=500)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

        assert result.output == "Failed to fetch data\n"
