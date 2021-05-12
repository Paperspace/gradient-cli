import os
import shutil
import tempfile

import mock
from click.testing import CliRunner

from gradient.api_sdk.clients.http_client import default_headers
from gradient.cli import cli
from tests import example_responses, MockResponse
from tests.example_responses import LIST_MODEL_FILES_RESPONSE_JSON

EXPECTED_HEADERS = default_headers.copy()
EXPECTED_HEADERS["ps_client_name"] = "gradient-cli"

EXPECTED_HEADERS_WITH_CHANGED_API_KEY = EXPECTED_HEADERS.copy()
EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"


class TestModelsList(object):
    URL = "https://api.paperspace.io/mlModels/getModelList/"
    COMMAND = ["models", "list"]

    COMMAND_WITH_FILTERING_BY_EXPERIMENT_ID = [
        "models", "list",
        "--experimentId", "some_experiment_id",
        "--projectId", "some_project_id",
        "--tag", "some_tag",
        "--tag", "some_other_tag",
    ]
    EXPECTED_REQUEST_JSON_WITH_FILTERING = {"filter": {"where": {"and": [{"projectId": "some_project_id",
                                                                          "experimentId": "some_experiment_id"}]}},
                                            "tagFilter": ("some_tag", "some_other_tag")}

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
        get_patched.return_value = MockResponse(example_responses.LIST_MODELS_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params={"limit": -1})

        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_replate_api_key_in_headers_when_api_key_parameter_was_used(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.LIST_MODELS_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_PARAMETER_USED)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params={"limit": -1})

        assert result.output == self.EXPECTED_STDOUT
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, get_patched, models_list_config_path):
        get_patched.return_value = MockResponse(example_responses.LIST_MODELS_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [models_list_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=self.EXPECTED_REQUEST_JSON_WITH_FILTERING,
                                            params={"limit": -1})

        assert result.output == self.EXPECTED_STDOUT
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_list_of_models_filtered_experiment_id(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.LIST_MODELS_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_FILTERING_BY_EXPERIMENT_ID)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=self.EXPECTED_REQUEST_JSON_WITH_FILTERING,
                                            params={"limit": -1})

        assert result.output == self.EXPECTED_STDOUT

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_proper_message_when_no_models_were_found(
            self, get_patched):
        get_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON_WHEN_NO_MODELS_WERE_FOUND)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params={"limit": -1})

        assert result.output == "No data found\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED, 401)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params={"limit": -1})

        assert result.output == "Failed to fetch data: No such API token\n"


class TestDeleteModel(object):
    URL = "https://api.paperspace.io/mlModels/deleteModel/"
    COMMAND = ["models", "delete", "--id", "some_id"]
    EXPECTED_REQUEST_JSON = {"id": "some_id"}

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
                                             headers=EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             files=None,
                                             data=None,
                                             params=None)

        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_replace_api_key_in_headers_when_api_key_parameter_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=204)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_PARAMETER_USED)

        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             files=None,
                                             data=None,
                                             params=None)

        assert result.output == self.EXPECTED_STDOUT
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, post_patched, models_delete_config_path):
        post_patched.return_value = MockResponse(status_code=204)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [models_delete_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             files=None,
                                             data=None,
                                             params=None)

        assert result.output == self.EXPECTED_STDOUT
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_and_print_proper_message_when_model_with_given_id_was_not_found(
            self, post_patched):
        post_patched.return_value = MockResponse(example_responses.DELETE_MODEL_404_RESPONSE_JSON, status_code=404)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
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
                                             headers=EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             files=None,
                                             data=None,
                                             params=None)

        assert result.output == "Failed to delete resource: Invalid API token\n"

class TestModelCreate(object):
    URL = "https://api.paperspace.io/mlModels/createModelV2"
    BASE_COMMAND = [
        "models", "create",
        "--name", "some_name",
        "--modelType", "custom",
        "--datasetRef", "dsr8k5qzn401lb5:latest",
    ]
    BASE_PARAMS = {
        "name": "some_name",
        "modelType": "Custom",
        "datasetRef": "dsr8k5qzn401lb5:latest"
    }
    COMMAND_WITH_ALL_OPTIONS = [
        "models", "create",
        "--name", "some_name",
        "--modelType", "tensorflow",
        "--modelSummary", """{"key": "value"}""",
        "--datasetRef", "dsr8k5qzn401lb5:latest",
        "--notes", "some notes",
        "--projectId", "some_project_id",
    ]
    ALL_OPTIONS_PARAMS = {
        "name": "some_name",
        "modelType": "Tensorflow",
        "summary": """{"key": "value"}""",
        "notes": "some notes",
        "projectId": "some_project_id",
        "datasetRef": "dsr8k5qzn401lb5:latest",
    }


    EXPECTED_STDOUT = "Model created with ID: some_model_id\n"

    CREATE_MODEL_V2_REPONSE = example_responses.MODEL_CREATE_RESPONSE_JSON_V2

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_when_models_create_command_was_used_with_basic_options(
            self, post_patched):
        post_patched.return_value = MockResponse(self.CREATE_MODEL_V2_REPONSE)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASE_COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_has_calls([
            mock.call(self.URL,
                        headers=EXPECTED_HEADERS,
                        json=None,
                        files=None,
                        data=None,
                        params=self.BASE_PARAMS),
        ])

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_when_models_update_command_was_used_with_all_options(
            self, post_patched):
        post_patched.return_value = MockResponse(self.CREATE_MODEL_V2_REPONSE)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_ALL_OPTIONS)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_has_calls([
            mock.call(self.URL,
                        headers=EXPECTED_HEADERS,
                        json=None,
                        files=None,
                        data=None,
                        params=self.ALL_OPTIONS_PARAMS),
        ])


class TestModelUpload(object):
    URL = "https://api.paperspace.io/mlModels/createModelV2"
    TAGS_URL = "https://api.paperspace.io/entityTags/updateTags"
    MODEL_FILE = "saved_model.pb"
    BASE_COMMAND = [
        "models", "upload",
        MODEL_FILE,
        "--name", "some_name",
        "--modelType", "custom",
    ]
    BASE_COMMAND_WITH_TAGS = [
        "models", "upload",
        MODEL_FILE,
        "--name", "some_name",
        "--modelType", "custom",
        "--tag", "test0",
        "--tag", "test1",
        "--tags", "test2,test3",
    ]
    BASE_PARAMS = {
        "name": "some_name",
        "modelType": "Custom",
    }
    TAGS_JSON = {
        "entity": "mlModel",
        "entityId": "some_model_id",
        "tags": ["test0", "test1", "test2", "test3"]
    }
    COMMAND_WITH_ALL_OPTIONS = [
        "models", "upload",
        MODEL_FILE,
        "--name", "some_name",
        "--modelType", "tensorflow",
        "--modelSummary", """{"key": "value"}""",
        "--notes", "some notes",
        "--projectId", "some_project_id",
        "--clusterId", "some_cluster_id",
    ]
    ALL_OPTIONS_PARAMS = {
        "name": "some_name",
        "modelType": "Tensorflow",
        "summary": """{"key": "value"}""",
        "notes": "some notes",
        "projectId": "some_project_id",
    }

    COMMAND_WITH_API_KEY_PARAMETER_USED = [
        "models", "upload",
        MODEL_FILE,
        "--name", "some_name",
        "--modelType", "tensorflow",
        "--modelSummary", """{"key": "value"}""",
        "--notes", "some notes",
        "--projectId", "some_project_id",
        "--clusterId", "some_cluster_id",
        "--apiKey", "some_key",
    ]
    COMMAND_WITH_OPTIONS_FILE = ["models", "upload", "--optionsFile", ]  # path added in test

    EXPECTED_STDOUT = "Model uploaded with ID: some_model_id\n"

    GET_PRESIGNED_URL = "https://api.paperspace.io/mlModels/getPresignedModelUrl"
    GET_PRESIGNED_URL_PARAMS = {"fileName": "saved_model.pb", "modelHandle": "some_model_id", "contentType": "", "clusterId": "some_cluster_id"}
    GET_PRESIGNED_URL_PARAMS_BASIC = {"fileName": "saved_model.pb", "modelHandle": "some_model_id", "contentType": ""}
    GET_PRESIGNED_URL_RESPONSE = example_responses.MODEL_UPLOAD_GET_PRESIGNED_URL_RESPONSE

    CREATE_MODEL_V2_REPONSE = example_responses.MODEL_CREATE_RESPONSE_JSON_V2

    EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED = {"status": 400, "message": "Invalid API token"}
    UPDATE_TAGS_RESPONSE_JSON_200 = example_responses.UPDATE_TAGS_RESPONSE

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_when_models_update_command_was_used_with_basic_options(
            self, post_patched, put_patched, get_patched):
        post_patched.return_value = MockResponse(self.CREATE_MODEL_V2_REPONSE)
        put_patched.return_value = MockResponse()
        get_patched.return_value = MockResponse(self.GET_PRESIGNED_URL_RESPONSE)

        runner = CliRunner()
        with runner.isolated_filesystem():
            with open(self.MODEL_FILE, "w") as h:
                h.write("I'm a model!")

            result = runner.invoke(cli.cli, self.BASE_COMMAND)

            assert result.output == self.EXPECTED_STDOUT, result.exc_info
            post_patched.assert_has_calls([
                mock.call(self.URL,
                          headers=EXPECTED_HEADERS,
                          json=None,
                          files=None,
                          data=None,
                          params=self.BASE_PARAMS),
            ])
            put_patched.assert_has_calls([
                mock.call(self.GET_PRESIGNED_URL_RESPONSE,
                          headers={"Content-Type": mock.ANY},
                          json=None,
                          params=None,
                          data=mock.ANY)
            ])
            get_patched.assert_called_once_with(self.GET_PRESIGNED_URL,
                                                headers=EXPECTED_HEADERS,
                                                params=self.GET_PRESIGNED_URL_PARAMS_BASIC,
                                                json=None,
                                                )
            assert put_patched.call_args.kwargs["data"].encoder.fields["file"][0] == self.MODEL_FILE

            assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_post_request_when_models_update_command_was_used_with_all_options(
            self, post_patched, put_patched, get_patched):
        post_patched.return_value = MockResponse(self.CREATE_MODEL_V2_REPONSE)
        put_patched.return_value = MockResponse()
        get_patched.return_value = MockResponse(self.GET_PRESIGNED_URL_RESPONSE)

        runner = CliRunner()
        with runner.isolated_filesystem():
            with open(self.MODEL_FILE, "w") as h:
                h.write("I'm a model!")

            result = runner.invoke(cli.cli, self.COMMAND_WITH_ALL_OPTIONS)

            assert result.output == self.EXPECTED_STDOUT, result.exc_info
            post_patched.assert_has_calls([
                mock.call(self.URL,
                          headers=EXPECTED_HEADERS,
                          json=None,
                          files=None,
                          data=None,
                          params=self.ALL_OPTIONS_PARAMS),
            ])
            put_patched.assert_has_calls([
                mock.call(self.GET_PRESIGNED_URL_RESPONSE,
                          headers={"Content-Type": mock.ANY},
                          json=None,
                          params=None,
                          data=mock.ANY)])
            get_patched.assert_called_once_with(self.GET_PRESIGNED_URL,
                                                headers=EXPECTED_HEADERS,
                                                params=self.GET_PRESIGNED_URL_PARAMS,
                                                json=None,
                                                )
            assert put_patched.call_args.kwargs["data"].encoder.fields["file"][0] == self.MODEL_FILE

            assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_replace_api_key_in_headers_when_api_key_parameter_was_used(
            self, post_patched, put_patched, get_patched):
        post_patched.return_value = MockResponse(self.CREATE_MODEL_V2_REPONSE)
        put_patched.return_value = MockResponse()
        get_patched.return_value = MockResponse(self.GET_PRESIGNED_URL_RESPONSE)

        runner = CliRunner()
        with runner.isolated_filesystem():
            with open(self.MODEL_FILE, "w") as h:
                h.write("I'm a model!")

            result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_PARAMETER_USED)

            assert result.output == self.EXPECTED_STDOUT, result.exc_info
            post_patched.assert_has_calls([
                mock.call(self.URL,
                          headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                          json=None,
                          files=None,
                          data=None,
                          params=self.ALL_OPTIONS_PARAMS
                          ),
            ])
            put_patched.assert_has_calls([
                mock.call(self.GET_PRESIGNED_URL_RESPONSE,
                          headers={"Content-Type": mock.ANY},
                          json=None,
                          params=None,
                          data=mock.ANY)
            ])
            get_patched.assert_called_once_with(self.GET_PRESIGNED_URL,
                                                headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                                params=self.GET_PRESIGNED_URL_PARAMS,
                                                json=None,
                                                )
            assert put_patched.call_args.kwargs["data"].encoder.fields["file"][0] == self.MODEL_FILE

            assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(
            self, post_patched, put_patched, get_patched, models_upload_config_path):
        post_patched.return_value = MockResponse(self.CREATE_MODEL_V2_REPONSE)
        put_patched.return_value = MockResponse()
        get_patched.return_value = MockResponse(self.GET_PRESIGNED_URL_RESPONSE)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [models_upload_config_path]

        runner = CliRunner()
        with runner.isolated_filesystem():
            with open(self.MODEL_FILE, "w") as h:
                h.write("I'm a model!")

            result = runner.invoke(cli.cli, command)

            assert result.output == self.EXPECTED_STDOUT, result.exc_info
            post_patched.assert_has_calls([
                mock.call(
                    self.URL,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                    json=None,
                    files=None,
                    data=None,
                    params=self.ALL_OPTIONS_PARAMS
                ),
            ])
            put_patched.assert_called_once_with(self.GET_PRESIGNED_URL_RESPONSE,
                                                headers={"Content-Type": ""},
                                                json=None,
                                                params=None,
                                                data=mock.ANY)
            get_patched.assert_called_once_with(self.GET_PRESIGNED_URL,
                                                headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                                params=self.GET_PRESIGNED_URL_PARAMS,
                                                json=None,
                                                )
            assert put_patched.call_args.kwargs["data"].encoder.fields["file"][0] == self.MODEL_FILE

            assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED, 401)

        runner = CliRunner()
        with runner.isolated_filesystem():
            with open(self.MODEL_FILE, "w") as h:
                h.write("I'm a model!")

            result = runner.invoke(cli.cli, self.BASE_COMMAND)

            assert result.output == "Failed to create resource: Invalid API token\n", result.exc_info
            post_patched.assert_called_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            files=None,
                                            data=None,
                                            params=self.BASE_PARAMS)

            assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_tag_machine(
            self, post_patched, put_patched, get_patched):
        post_patched.return_value = MockResponse(self.CREATE_MODEL_V2_REPONSE)
        put_patched.return_value = MockResponse()
        get_patched.side_effect = [MockResponse(self.GET_PRESIGNED_URL_RESPONSE),
                                   MockResponse({})]

        runner = CliRunner()
        with runner.isolated_filesystem():
            with open(self.MODEL_FILE, "w") as h:
                h.write("I'm a model!")

            result = runner.invoke(cli.cli, self.BASE_COMMAND_WITH_TAGS)
            assert result.output == self.EXPECTED_STDOUT, result.exc_info
            post_patched.assert_has_calls([
                mock.call(self.URL,
                          headers=EXPECTED_HEADERS,
                          json=None,
                          files=None,
                          data=None,
                          params=self.BASE_PARAMS
                          ),
            ])

            get_patched.assert_has_calls(
                [
                    mock.call(
                        self.GET_PRESIGNED_URL,
                        headers=EXPECTED_HEADERS,
                        params=self.GET_PRESIGNED_URL_PARAMS_BASIC,
                        json=None,
                    ),
                ]
            )
            put_patched.assert_has_calls(
                [
                    mock.call(
                        self.GET_PRESIGNED_URL_RESPONSE,
                        headers={"Content-Type": mock.ANY},
                        json=None,
                        params=None,
                        data=mock.ANY,
                    ),
                    mock.call(
                        self.TAGS_URL,
                        headers=EXPECTED_HEADERS,
                        json=self.TAGS_JSON,
                        params=None,
                        data=None,
                    ),
                ]
            )

            assert EXPECTED_HEADERS["X-API-Key"] != "some_key"


class TestModelDetails(object):
    URL = "https://api.paperspace.io/mlModels/getModelList/"
    COMMAND = ["models", "details", "--id", "some_id"]

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
| Tags             |                                                                            |
+------------------+----------------------------------------------------------------------------+
"""

    EXPECTED_STDOUT_WITH_TAGS = """+------------------+----------------------------------------------------------------------------+
| ID               | some_id                                                                    |
+------------------+----------------------------------------------------------------------------+
| Name             | some_name                                                                  |
| Project ID       | some_project_id                                                            |
| Experiment ID    | some_experiment_id                                                         |
| Model Type       | Tensorflow                                                                 |
| URL              | s3://ps-projects-development/asdf/some_project_id/some_experiment_id/model |
| Deployment State | Stopped                                                                    |
| Tags             | tag1, tag2                                                                 |
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
                                            headers=EXPECTED_HEADERS,
                                            json=self.EXPECTED_REQUEST_JSON,
                                            params=None)

        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_details_of_experiment_that_has_some_tags(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.MODEL_DETAILS_RESPONSE_JSON_WITH_TAGS)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WITH_TAGS, result.exc_info
        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=self.EXPECTED_REQUEST_JSON,
                                            params=None)

        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_replace_api_key_in_headers_when_api_key_parameter_was_used(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.MODEL_DETAILS_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_PARAMETER_USED)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=self.EXPECTED_REQUEST_JSON,
                                            params=None)

        assert result.output == self.EXPECTED_STDOUT
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, get_patched, models_details_config_path):
        get_patched.return_value = MockResponse(example_responses.MODEL_DETAILS_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [models_details_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=self.EXPECTED_REQUEST_JSON,
                                            params=None)

        assert result.output == self.EXPECTED_STDOUT
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_proper_message_when_no_models_were_found(
            self, get_patched):
        get_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON_WHEN_NO_MODELS_WERE_FOUND)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=self.EXPECTED_REQUEST_JSON,
                                            params=None)

        assert result.output == "Model not found\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_WHEN_WRONG_API_KEY_WAS_USED, 401)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=self.EXPECTED_REQUEST_JSON,
                                            params=None)

        assert result.output == "Failed to fetch data: Invalid API token\n"


class TestDownloadModelFiles(object):
    runner = CliRunner()
    LIST_FILES_URL = "https://api.paperspace.io/mlModels/listFiles/"
    DESTINATION_DIR_NAME = "dest"
    DESTINATION_DIR_PATH = os.path.join(tempfile.gettempdir(), "dest")

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
                      headers=EXPECTED_HEADERS,
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
