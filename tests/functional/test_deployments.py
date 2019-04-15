import mock
from click.testing import CliRunner

import paperspace.client
from paperspace import cli
from paperspace.commands import deployments as deployments_commands
from tests import example_responses, MockResponse

EXPECTED_HEADERS = deployments_commands.default_headers


class TestDeploymentsCreate(object):
    URL = "https://api.paperspace.io/deployments/createDeployment/"
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"
    BASIC_OPTIONS_COMMAND = [
        "deployments", "create",
        "--deploymentType", "tfserving",
        "--modelId", "some_model_id",
        "--name", "some_name",
        "--machineType", "Air",
        "--imageUrl", "https://www.latlmes.com/breaking/paperspace-now-has-a-100-bilion-valuation",
        "--instanceCount", "666",
    ]
    BASIC_OPTIONS_COMMAND_WITH_API_KEY = [
        "deployments", "create",
        "--deploymentType", "tfserving",
        "--modelId", "some_model_id",
        "--name", "some_name",
        "--machineType", "Air",
        "--imageUrl", "https://www.latlmes.com/breaking/paperspace-now-has-a-100-bilion-valuation",
        "--instanceCount", "666",
        "--apiKey", "some_key",
    ]
    BASIC_OPTIONS_REQUEST = {
        "machineType": u"Air",
        "name": u"some_name",
        "imageUrl": u"https://www.latlmes.com/breaking/paperspace-now-has-a-100-bilion-valuation",
        "deploymentType": "Tensorflow Serving on K8s",
        "instanceCount": 666,
        "modelId": u"some_model_id",
    }
    RESPONSE_JSON_200 = example_responses.CREATE_DEPLOYMENT_WITH_BASIC_OPTIONS_RESPONSE
    EXPECTED_STDOUT = "New deployment created with id: sadkfhlskdjh\n"

    RESPONSE_JSON_404_MODEL_NOT_FOUND = {"error": {"name": "Error", "status": 404, "message": "Unable to find model"}}
    RESPONSE_CONTENT_404_MODEL_NOT_FOUND = b'{"error":{"name":"Error","status":404,"message":"Unable to find model"}}\n'
    EXPECTED_STDOUT_MODEL_NOT_FOUND = "Unable to find model\n"

    @mock.patch("paperspace.cli.deployments_commands.client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_deployment_with_basic_options(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.cli.deployments_commands.client.requests.post")
    def test_should_send_different_api_key_when_api_key_parameter_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND_WITH_API_KEY)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.cli.deployments_commands.client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_wrong_model_id_was_given(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_404_MODEL_NOT_FOUND, 404,
                                                 self.RESPONSE_CONTENT_404_MODEL_NOT_FOUND)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None)
        assert result.output == self.EXPECTED_STDOUT_MODEL_NOT_FOUND
        assert result.exit_code == 0


class TestDeploymentsList(object):
    URL = "https://api.paperspace.io/deployments/getDeploymentList/"

    COMMAND = ["deployments", "list"]
    LIST_JSON = example_responses.LIST_DEPLOYMENTS

    COMMAND_WITH_API_KEY = ["deployments", "list", "--apiKey", "some_key"]
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    COMMAND_WITH_FILTER_WITH_STATE = ["deployments", "list", "--state", "Stopped"]
    LIST_WITH_FILTER_REQUEST_JSON = {"filter": {"where": {"and": [{"state": "Stopped"}]}}}
    LIST_WITH_FILTER_RESPONSE_JSON_WHEN_NO_DEPLOYMENTS_FOUND = {"deploymentList": [], "total": 17, "displayTotal": 0,
                                                                "runningTotal": 0}
    DETAILS_STDOUT = """+-----------+-----------------+----------------------------------------------------------------------------------+---------------+---------------------------+
| Name      | ID              | Endpoint                                                                         | Api Type      | Deployment Type           |
+-----------+-----------------+----------------------------------------------------------------------------------+---------------+---------------------------+
| some_name | dev61ity7lx232  | https://development-services.paperspace.io/model-serving/dev61ity7lx232:predict  | some_api_type | Tensorflow Serving on K8s |
| some_name | desanw1jptk7woh | https://development-services.paperspace.io/model-serving/desanw1jptk7woh:predict | REST          | Tensorflow Serving on K8s |
| some_name | desfnnrqt1v633v | https://development-services.paperspace.io/model-serving/desfnnrqt1v633v:predict | REST          | Tensorflow Serving on K8s |
| some_name | desdyn55d2e02su | https://development-services.paperspace.io/model-serving/desdyn55d2e02su:predict | REST          | Tensorflow Serving on K8s |
| some_name | des3tmqa3s627o9 | https://development-services.paperspace.io/model-serving/des3tmqa3s627o9:predict | REST          | Tensorflow Serving on K8s |
+-----------+-----------------+----------------------------------------------------------------------------------+---------------+---------------------------+
"""

    @mock.patch("paperspace.cli.deployments_commands.client.requests.get")
    def test_should_send_get_request_and_print_list_of_deployments(self, get_patched):
        get_patched.return_value = MockResponse(self.LIST_JSON, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None)
        assert result.output == self.DETAILS_STDOUT

    @mock.patch("paperspace.cli.deployments_commands.client.requests.get")
    def test_should_send_get_request_with_custom_api_key_when_api_key_parameter_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(self.LIST_JSON, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=None)
        assert result.output == self.DETAILS_STDOUT

    @mock.patch("paperspace.cli.deployments_commands.pydoc")
    @mock.patch("paperspace.cli.deployments_commands.client.requests.get")
    def test_should_send_get_request_and_paginate_list_when_output_table_len_is_gt_lines_in_terminal(self, get_patched,
                                                                                                     pydoc_patched):
        list_json = {"deploymentList": self.LIST_JSON["deploymentList"] * 40}
        get_patched.return_value = MockResponse(list_json, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None)
        pydoc_patched.pager.assert_called_once()
        assert result.exit_code == 0

    @mock.patch("paperspace.cli.deployments_commands.client.requests.get")
    def test_should_send_get_request_and_print_list_of_deployments_filtered_by_state(self, get_patched):
        get_patched.return_value = MockResponse(self.LIST_JSON, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_FILTER_WITH_STATE)

        get_patched.assert_called_with("https://api.paperspace.io/deployments/getDeploymentList/",
                                       headers=EXPECTED_HEADERS,
                                       json=self.LIST_WITH_FILTER_REQUEST_JSON,
                                       params=None)
        assert result.output == self.DETAILS_STDOUT

    @mock.patch("paperspace.cli.deployments_commands.client.requests.get")
    def test_should_send_get_request_and_print_list_of_deployments_filtered_with_state_but_none_found(
            self, get_patched):
        get_patched.return_value = MockResponse(self.LIST_WITH_FILTER_RESPONSE_JSON_WHEN_NO_DEPLOYMENTS_FOUND, 200,
                                                "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_FILTER_WITH_STATE)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=self.LIST_WITH_FILTER_REQUEST_JSON,
                                            params=None)
        assert result.output == "No deployments found\n"


class TestDeploymentsUpdate(object):
    URL = "https://api.paperspace.io/deployments/updateDeployment/"
    COMMAND = [
        "deployments", "update",
        "--id", "some_id",
        "--name", "new_name",
    ]
    BASIC_OPTIONS_REQUEST_JSON = {"upd": {"name": u"new_name"}, "id": u"some_id"}

    COMMAND_WITH_API_KEY = [
        "deployments", "update",
        "--id", "some_id",
        "--name", "new_name",
        "--apiKey", "some_key"
    ]
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    RESPONSE_JSON_200 = {"upd": {"name": u"asd"}, "id": u"dennaw0wzbvvg3"}
    EXPECTED_STDOUT = "Deployment model updated.\n"

    RESPONSE_JSON_400 = {"error": {"name": "Error", "status": 400, "message": "Unable to access deployment"}}
    EXPECTED_STDOUT_WITH_WRONG_ID = "Unable to access deployment\n"

    @mock.patch("paperspace.cli.deployments_commands.client.requests.post")
    def test_should_send_proper_data_and_print_message_when_update_deployment(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST_JSON,
                                             params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.cli.deployments_commands.client.requests.post")
    def test_should_send_proper_data_with_custom_api_key_when_api_key_parameter_was_provided(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.BASIC_OPTIONS_REQUEST_JSON,
                                             params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.cli.deployments_commands.client.requests.post")
    def test_should_send_proper_data_and_print_message_when_update_deployment_used_with_wrong_id(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_400, 400, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST_JSON,
                                             params=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_ID
        assert result.exit_code == 0


class TestStartDeployment(object):
    URL = "https://api.paperspace.io/deployments/updateDeployment/"
    COMMAND = ["deployments", "start",
               "--id", "some_id"]
    REQUEST_JSON = {"isRunning": True, "id": u"some_id"}
    EXPECTED_STDOUT = "Deployment started\n"

    @mock.patch("paperspace.cli.deployments_commands.client.requests.post")
    def test_should_send_proper_data_and_print_message_when_deployments_start_was_used(self, post_patched):
        post_patched.return_value = MockResponse(None, 204, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.REQUEST_JSON,
                                             params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0


class TestDeleteDeployment(object):
    URL = "https://api.paperspace.io/deployments/updateDeployment/"
    COMMAND = ["deployments", "delete",
               "--id", "some_id"]
    REQUEST_JSON = {"upd": {"isDeleted": True}, "id": u"some_id"}
    EXPECTED_STDOUT = "Deployment deleted.\n"

    COMMAND_WITH_API_KEY = [
        "deployments", "delete",
        "--id", "some_id",
        "--apiKey", "some_key",
    ]
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    RESPONSE_JSON_400 = {"error": {"name": "Error", "status": 400, "message": "Unable to access deployment"}}
    EXPECTED_STDOUT_WITH_WRONG_ID = "Unable to access deployment\n"

    @mock.patch("paperspace.cli.deployments_commands.client.requests.post")
    def test_should_send_proper_data_and_print_message_when_deployments_delete_was_used(self, post_patched):
        post_patched.return_value = MockResponse(None, 204, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.REQUEST_JSON,
                                             params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.cli.deployments_commands.client.requests.post")
    def test_should_send_proper_data_with_custom_api_key_when_api_key_parameter_was_provided(self, post_patched):
        post_patched.return_value = MockResponse(None, 204, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.REQUEST_JSON,
                                             params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.cli.deployments_commands.client.requests.post")
    def test_should_send_proper_data_and_print_message_when_deployments_delete_used_with_wrong_id(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_400, 400, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.REQUEST_JSON,
                                             params=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_ID
        assert result.exit_code == 0
