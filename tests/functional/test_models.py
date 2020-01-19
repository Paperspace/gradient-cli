import os
import shutil
import tempfile

import mock
from click.testing import CliRunner

import gradient.api_sdk.clients.http_client
from gradient.cli import cli
from tests import example_responses, MockResponse
from tests.example_responses import LIST_MODEL_FILES_RESPONSE_JSON


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


class TestDeleteModel(object):
    URL = "https://api.paperspace.io/mlModels/deleteModel/"
    COMMAND = ["models", "delete", "--id", "some_id"]
    EXPECTED_REQUEST_JSON = {"id": "some_id"}

    EXPECTED_HEADERS = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    COMMAND_WITH_API_KEY_PARAMETER_USED = ["models", "delete", "--id", "some_id", "--apiKey", "some_key"]
    COMMAND_WITH_OPTIONS_FILE = ["models", "delete", "--id", "some_id", "--optionsFile", ]  # path added in test

    EXPECTED_STDOUT = "Model deleted\n"

    EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED = {"status": 400, "message": "Invalid API token"}

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_when_models_delete_command_was_executed(self, post_patched):
        post_patched.return_value = MockResponse(status_code=204)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             files=None,
                                             data=None,
                                             params=None)

        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_replace_api_key_in_headers_when_api_key_parameter_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=204)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_PARAMETER_USED)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             files=None,
                                             data=None,
                                             params=None)

        assert result.output == self.EXPECTED_STDOUT
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, post_patched, models_delete_config_path):
        post_patched.return_value = MockResponse(status_code=204)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [models_delete_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             files=None,
                                             data=None,
                                             params=None)

        assert result.output == self.EXPECTED_STDOUT
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_and_print_proper_message_when_model_with_given_id_was_not_found(
            self, post_patched):
        post_patched.return_value = MockResponse(example_responses.DELETE_MODEL_404_RESPONSE_JSON, status_code=404)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             files=None,
                                             data=None,
                                             params=None)

        assert result.output == "Failed to delete resource: Unable to find model\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED, 401)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             files=None,
                                             data=None,
                                             params=None)

        assert result.output == "Failed to delete resource: Invalid API token\n"


class TestModelUpload(object):
    URL = "https://api.paperspace.io/mlModels/createModel"
    MODEL_FILE = "saved_model.pb"
    BASE_COMMAND = [
        "models", "upload",
        MODEL_FILE,
        "--name", "some_name",
        "--modelType", "tensorflow",
    ]
    BASE_PARAMS = {
        "name": "some_name",
        "modelType": "Tensorflow",
    }
    COMMAND_WITH_ALL_OPTIONS = [
        "models", "upload",
        MODEL_FILE,
        "--name", "some_name",
        "--modelType", "tensorflow",
        "--modelSummary", """{"key": "value"}""",
        "--notes", "some notes",
    ]
    ALL_OPTIONS_PARAMS = {
        "name": "some_name",
        "modelType": "Tensorflow",
        "summary": """{"key": "value"}""",
        "notes": "some notes",
    }

    EXPECTED_HEADERS = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    COMMAND_WITH_API_KEY_PARAMETER_USED = [
        "models", "upload",
        MODEL_FILE,
        "--name", "some_name",
        "--modelType", "tensorflow",
        "--modelSummary", """{"key": "value"}""",
        "--notes", "some notes",
        "--apiKey", "some_key",
    ]
    COMMAND_WITH_OPTIONS_FILE = ["models", "upload", "--optionsFile", ]  # path added in test

    EXPECTED_STDOUT = "Model uploaded with ID: some_model_id\n"

    EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED = {"status": 400, "message": "Invalid API token"}

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_when_models_update_command_was_used_with_basic_options(self, post_patched):
        post_patched.return_value = MockResponse(json_data=example_responses.MODEL_UPLOAD_RESPONSE_JSON)

        runner = CliRunner()
        with runner.isolated_filesystem():
            with open(self.MODEL_FILE, "w") as h:
                h.write("I'm a model!")

            result = runner.invoke(cli.cli, self.BASE_COMMAND)

            assert result.output == self.EXPECTED_STDOUT, result.exc_info
            post_patched.assert_called_once_with(self.URL,
                                                 headers=self.EXPECTED_HEADERS,
                                                 json=None,
                                                 files=[(self.MODEL_FILE, mock.ANY)],
                                                 data=None,
                                                 params=self.BASE_PARAMS)
            assert post_patched.call_args.kwargs["files"][0][1].name == self.MODEL_FILE
            assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_when_models_update_command_was_used_with_all_options(self, post_patched):
        post_patched.return_value = MockResponse(json_data=example_responses.MODEL_UPLOAD_RESPONSE_JSON)

        runner = CliRunner()
        with runner.isolated_filesystem():
            with open(self.MODEL_FILE, "w") as h:
                h.write("I'm a model!")

            result = runner.invoke(cli.cli, self.COMMAND_WITH_ALL_OPTIONS)

            assert result.output == self.EXPECTED_STDOUT, result.exc_info
            post_patched.assert_called_once_with(self.URL,
                                                 headers=self.EXPECTED_HEADERS,
                                                 json=None,
                                                 files=[(self.MODEL_FILE, mock.ANY)],
                                                 data=None,
                                                 params=self.ALL_OPTIONS_PARAMS)

            assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_replace_api_key_in_headers_when_api_key_parameter_was_used(self, post_patched):
        post_patched.return_value = MockResponse(json_data=example_responses.MODEL_UPLOAD_RESPONSE_JSON)

        runner = CliRunner()
        with runner.isolated_filesystem():
            with open(self.MODEL_FILE, "w") as h:
                h.write("I'm a model!")

            result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_PARAMETER_USED)

            post_patched.assert_called_once_with(self.URL,
                                                 headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                                 json=None,
                                                 files=[(self.MODEL_FILE, mock.ANY)],
                                                 data=None,
                                                 params=self.ALL_OPTIONS_PARAMS)

            assert result.output == self.EXPECTED_STDOUT
            assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, post_patched, models_upload_config_path):
        post_patched.return_value = MockResponse(json_data=example_responses.MODEL_UPLOAD_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [models_upload_config_path]

        runner = CliRunner()
        with runner.isolated_filesystem():
            with open(self.MODEL_FILE, "w") as h:
                h.write("I'm a model!")

            result = runner.invoke(cli.cli, command)

            post_patched.assert_called_once_with(self.URL,
                                                 headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                                 json=None,
                                                 files=[(self.MODEL_FILE, mock.ANY)],
                                                 data=None,
                                                 params=self.ALL_OPTIONS_PARAMS)

            assert result.output == self.EXPECTED_STDOUT
            assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED, 401)

        runner = CliRunner()
        with runner.isolated_filesystem():
            with open(self.MODEL_FILE, "w") as h:
                h.write("I'm a model!")

            result = runner.invoke(cli.cli, self.BASE_COMMAND)

            post_patched.assert_called_once_with(self.URL,
                                                 headers=self.EXPECTED_HEADERS,
                                                 json=None,
                                                 files=[(self.MODEL_FILE, mock.ANY)],
                                                 data=None,
                                                 params=self.BASE_PARAMS)

            assert result.output == "Failed to create resource: Invalid API token\n"


class TestModelDetails(object):
    URL = "https://api.paperspace.io/mlModels/getModelList/"
    COMMAND = ["models", "details", "--id", "some_id"]
    EXPECTED_HEADERS = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    EXPECTED_REQUEST_JSON = {"filter": {"where": {"and": [{"id": "some_id"}]}}}

    COMMAND_WITH_API_KEY_PARAMETER_USED = ["models", "details", "--id", "some_id", "--apiKey", "some_key"]
    COMMAND_WITH_OPTIONS_FILE = ["models", "details", "--optionsFile", ]  # path added in test

    EXPECTED_RESPONSE_JSON_WHEN_NO_MODELS_WERE_FOUND = {"modelList": [], "total": 1, "displayTotal": 0}

    EXPECTED_STDOUT = """+------------------+----------------------------------------------------------------------------+
| ID               | some_id                                                                    |
+------------------+----------------------------------------------------------------------------+
| Name             | some_name                                                                  |
| Project ID       | some_project_id                                                            |
| Experiment ID    | some_experiment_id                                                         |
| Model Type       | Tensorflow                                                                 |
| URL              | s3://ps-projects-development/asdf/some_project_id/some_experiment_id/model |
| Deployment State | Stopped                                                                    |
+------------------+----------------------------------------------------------------------------+
"""

    EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED = {"status": 400, "message": "Invalid API token"}

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_details_of_experiment(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.MODEL_DETAILS_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=self.EXPECTED_REQUEST_JSON,
                                            params=None)

        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_replace_api_key_in_headers_when_api_key_parameter_was_used(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.MODEL_DETAILS_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_PARAMETER_USED)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=self.EXPECTED_REQUEST_JSON,
                                            params=None)

        assert result.output == self.EXPECTED_STDOUT
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, get_patched, models_details_config_path):
        get_patched.return_value = MockResponse(example_responses.MODEL_DETAILS_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [models_details_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=self.EXPECTED_REQUEST_JSON,
                                            params=None)

        assert result.output == self.EXPECTED_STDOUT
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_proper_message_when_no_models_were_found(
            self, get_patched):
        get_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON_WHEN_NO_MODELS_WERE_FOUND, 200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=self.EXPECTED_REQUEST_JSON,
                                            params=None)

        assert result.output == "Model not found\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED, 401)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=self.EXPECTED_REQUEST_JSON,
                                            params=None)

        assert result.output == "Failed to fetch data: Invalid API token\n"


class TestDownloadModelFiles(object):
    runner = CliRunner()
    LIST_FILES_URL = "https://api.paperspace.io/mlModels/listFiles/"
    DESTINATION_DIR_NAME = "dest"
    DESTINATION_DIR_PATH = os.path.join(tempfile.gettempdir(), "dest")
    EXPECTED_HEADERS = gradient.api_sdk.clients.http_client.default_headers.copy()

    COMMAND = ["models", "download", "--id", "some_model_id", "--destinationDir", DESTINATION_DIR_PATH]

    @classmethod
    def teardown_method(cls):
        shutil.rmtree(cls.DESTINATION_DIR_PATH)

    @mock.patch("gradient.api_sdk.s3_downloader.requests.get")
    def test_should_get_a_list_of_files_and_download_them_to_defined_directory_when_download_command_was_executed(
            self, get_patched,
    ):
        file_response_mock = mock.MagicMock()
        file_response_mock.content = "\"Hello Paperspace!\n\""
        file_response_mock_2 = mock.MagicMock()
        file_response_mock_2.content = "\"Hello Paperspace 2\n\""
        file_response_mock_3 = mock.MagicMock()
        file_response_mock_3.content = "\"Elo\n\""
        get_patched.side_effect = [
            MockResponse(LIST_MODEL_FILES_RESPONSE_JSON),
            file_response_mock,
            file_response_mock_2,
            file_response_mock_3,
        ]

        result = self.runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_has_calls([
            mock.call(self.LIST_FILES_URL,
                      headers=self.EXPECTED_HEADERS,
                      json={"links": True, "id": "some_model_id"},
                      params=None),
            mock.call("https://ps-projects.s3.amazonaws.com/some/path/model/hello.txt?AWSAccessKeyId="
                      "some_aws_access_key_id&Expires=713274132&Signature=7CT5k6buEmZe5k5E7g6BXMs2xV4%3D&"
                      "response-content-disposition=attachment%3Bfilename%3D%22hello.txt%22&x-amz-security-token="
                      "some_amz_security_token"),
            mock.call("https://ps-projects.s3.amazonaws.com/some/path/model/hello2.txt?AWSAccessKeyId="
                      "some_aws_access_key_id&Expires=713274132&Signature=L1lI47cNyiROzdYkf%2FF3Cm3165E%3D&"
                      "response-content-disposition=attachment%3Bfilename%3D%22hello2.txt%22&x-amz-security-token="
                      "some_amz_security_token"),
            mock.call("https://ps-projects.s3.amazonaws.com/some/path/model/keton/elo.txt?AWSAccessKeyId="
                      "some_aws_access_key_id&Expires=713274132&Signature=tHriojGx03S%2FKkVGQGVI5CQRFTo%3D&"
                      "response-content-disposition=attachment%3Bfilename%3D%22elo.txt%22&x-amz-security-token="
                      "some_amz_security_token"),
        ])
        assert os.path.exists(self.DESTINATION_DIR_PATH)
        assert os.path.isdir(self.DESTINATION_DIR_PATH)
        assert os.path.exists(os.path.join(self.DESTINATION_DIR_PATH, "keton"))
        assert os.path.isdir(os.path.join(self.DESTINATION_DIR_PATH, "keton"))

        hello_txt_path = os.path.join(self.DESTINATION_DIR_PATH, "hello.txt")
        assert os.path.exists(hello_txt_path)
        assert not os.path.isdir(hello_txt_path)
        with open(hello_txt_path) as h:
            assert h.read() == "\"Hello Paperspace!\n\""

        hello2_txt_path = os.path.join(self.DESTINATION_DIR_PATH, "hello2.txt")
        assert os.path.exists(hello2_txt_path)
        assert not os.path.isdir(hello2_txt_path)
        with open(hello2_txt_path) as h:
            assert h.read() == "\"Hello Paperspace 2\n\""

        elo_txt_path = os.path.join(self.DESTINATION_DIR_PATH, "keton", "elo.txt")
        assert os.path.exists(elo_txt_path)
        assert not os.path.isdir(elo_txt_path)
        with open(elo_txt_path) as h:
            assert h.read() == "\"Elo\n\""

        assert result.exit_code == 0
