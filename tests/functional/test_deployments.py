import json

import mock
import pytest
from click.testing import CliRunner

from gradient.api_sdk import sdk_exceptions, utils
from gradient.api_sdk.clients.http_client import default_headers
from gradient.cli import cli
from tests import example_responses, MockResponse

EXPECTED_HEADERS = default_headers.copy()
EXPECTED_HEADERS["ps_client_name"] = "gradient-cli"

EXPECTED_HEADERS_WITH_CHANGED_API_KEY = EXPECTED_HEADERS.copy()
EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"


@pytest.fixture
def basic_options_metrics_stream_websocket_connection_iterator():
    def generator(self):
        yield """{"handle": "desgffa3mtgepvm", "object_type": "modelDeployment", "chart_name": "memoryUsage",
               "pod_metrics": {"desgffa3mtgepvm-0": {"time_stamp": 1587673818, "value": "34914304"},
                               "desgffa3mtgepvm-1": {"time_stamp": 1587673818, "value": "35942400"}}}"""
        yield """{"handle": "desgffa3mtgepvm", "object_type": "modelDeployment", "chart_name": "cpuPercentage",
               "pod_metrics": {"desgffa3mtgepvm-0": {"time_stamp": 1587673818, "value": "0.044894188888835944"},
                               "desgffa3mtgepvm-1": {"time_stamp": 1587673818, "value": "0.048185748888916656"}}}"""
        yield """{"handle": "desgffa3mtgepvm", "object_type": "modelDeployment", "chart_name": "memoryUsage",
               "pod_metrics": {"desgffa3mtgepvm-0": {"time_stamp": 1587673820, "value": "34914304"},
                               "desgffa3mtgepvm-1": {"time_stamp": 1587673820, "value": "35942400"}}}"""

        raise sdk_exceptions.EndWebsocketStream()

    return generator


@pytest.fixture
def all_options_metrics_stream_websocket_connection_iterator():
    def generator(self):
        yield """{"handle": "desgffa3mtgepvm",
               "object_type": "modelDeployment",
               "chart_name": "gpuMemoryUsed",
               "pod_metrics": {"desgffa3mtgepvm-0": {"time_stamp": 1587640736, "value": "0"},
                               "desgffa3mtgepvm-1": {"time_stamp": 1587640736, "value": "0"}}}"""
        yield """{"handle": "desgffa3mtgepvm",
               "object_type": "modelDeployment",
               "chart_name": "gpuMemoryUsed",
               "pod_metrics": {"desgffa3mtgepvm-0": {"time_stamp": 1587640738, "value": "321"},
                               "desgffa3mtgepvm-1": {"time_stamp": 1587640738, "value": "432"}}}"""
        yield """{"handle": "desgffa3mtgepvm",
               "object_type": "modelDeployment",
               "chart_name": "gpuMemoryFree",
               "pod_metrics": {"desgffa3mtgepvm-0": {"time_stamp": 1587640740, "value": "1234"},
                               "desgffa3mtgepvm-1": {"time_stamp": 1587640740, "value": "234"}}}"""

        raise sdk_exceptions.EndWebsocketStream()

    return generator


class TestDeploymentsCreate(object):
    URL = "https://api.paperspace.io/deployments/createDeployment/"
    GET_PRESIGNED_URL = "https://api.paperspace.io/deployments/getPresignedDeploymentUrl"
    TAGS_URL = "https://api.paperspace.io/entityTags/updateTags"
    URL_V2 = "https://api.paperspace.io/deployments/v2/createDeployment/"
    VALIDATE_CLUSTER_URL = "https://api.paperspace.io/clusters/getCluster"
    BASIC_OPTIONS_COMMAND = [
        "deployments", "create",
        "--deploymentType", "tfserving",
        "--modelId", "some_model_id",
        "--name", "some_name",
        "--machineType", "G1",
        "--imageUrl", "https://www.latlmes.com/breaking/paperspace-now-has-a-100-bilion-valuation",
        "--instanceCount", "666",
    ]
    BASIC_OPTIONS_COMMAND_WITH_CURRENT_DIR_AS_WORKSPACE = [
        "deployments", "create",
        "--deploymentType", "tfserving",
        "--modelId", "some_model_id",
        "--name", "some_name",
        "--machineType", "G1",
        "--imageUrl", "https://www.latlmes.com/breaking/paperspace-now-has-a-100-bilion-valuation",
        "--instanceCount", "666",
        "--workspace", ".",
    ]
    BASIC_OPTIONS_COMMAND_WITH_TAGS = [
        "deployments", "create",
        "--deploymentType", "tfserving",
        "--modelId", "some_model_id",
        "--name", "some_name",
        "--machineType", "G1",
        "--imageUrl", "https://www.latlmes.com/breaking/paperspace-now-has-a-100-bilion-valuation",
        "--instanceCount", "666",
        "--tag", "test0",
        "--tag", "test1",
        "--tags", "test2,test3",
    ]
    BASIC_OPTIONS_COMMAND_WITH_CLUSTER_ID = [
        "deployments", "create",
        "--deploymentType", "tfserving",
        "--modelId", "some_model_id",
        "--name", "some_name",
        "--machineType", "G1",
        "--imageUrl", "https://www.latlmes.com/breaking/paperspace-now-has-a-100-bilion-valuation",
        "--instanceCount", "666",
        "--clusterId", "some_cluster_id",
    ]
    BASIC_OPTIONS_COMMAND_WITH_API_KEY = [
        "deployments", "create",
        "--deploymentType", "tfserving",
        "--modelId", "some_model_id",
        "--name", "some_name",
        "--machineType", "G1",
        "--imageUrl", "https://www.latlmes.com/breaking/paperspace-now-has-a-100-bilion-valuation",
        "--instanceCount", "666",
        "--apiKey", "some_key",
    ]
    COMMAND_WITH_ALL_OPTIONS = [
        "deployments", "create",
        "--deploymentType", "tfserving",
        "--projectId", "some_project_id",
        "--modelId", "some_model_id",
        "--name", "some_name",
        "--machineType", "G1",
        "--imageUrl", "https://www.latlmes.com/breaking/paperspace-now-has-a-100-bilion-valuation",
        "--instanceCount", "666",
        "--command", "some deployment command",
        "--containerModelPath", "some/container/model/path",
        "--imageUsername", "some_image_username",
        "--imagePassword", "some_image_password",
        "--imageServer", "some.image/server",
        "--containerUrlPath", "some/container/url/path",
        "--method", "some_method",
        "--dockerArgs", """["some", "docker", "args"]""",
        "--env", """{"key":"value"}""",
        "--apiType", "REST",
        "--ports", "5000,6000:7000",
        "--authUsername", "some_username",
        "--authPassword", "some_password",
        "--clusterId", "some_cluster_id",
        "--apiKey", "some_key",
        "--workspace", "s3://some-workspace",
        "--workspaceRef", "some_branch_name",
        "--workspaceUsername", "username",
        "--workspacePassword", "password",
    ]
    COMMAND_WITH_OPTIONS_FILE = ["deployments", "create", "--optionsFile", ]  # path added in test
    BASIC_OPTIONS_COMMAND_WITH_AUTOSCALING = [
        "deployments", "create",
        "--deploymentType", "tfserving",
        "--modelId", "some_model_id",
        "--name", "some_name",
        "--machineType", "G1",
        "--imageUrl", "https://www.latlmes.com/breaking/paperspace-now-has-a-100-bilion-valuation",
        "--instanceCount", "666",
        "--minInstanceCount", "4",
        "--maxInstanceCount", "64",
        "--scaleCooldownPeriod", "123",
        "--resource", "cpu/targetAverage:10",
        "--metric", "loss/target:2.0",
        "--metric", "keton/target:21.37",
    ]

    BASIC_OPTIONS_REQUEST = {
        "machineType": u"G1",
        "name": u"some_name",
        "imageUrl": u"https://www.latlmes.com/breaking/paperspace-now-has-a-100-bilion-valuation",
        "deploymentType": "TFServing",
        "instanceCount": 666,
        "modelId": u"some_model_id",
    }
    BASIC_OPTIONS_REQUEST_WHEN_CLUSTER_ID_WAS_SET = {
        "machineType": u"G1",
        "name": u"some_name",
        "imageUrl": u"https://www.latlmes.com/breaking/paperspace-now-has-a-100-bilion-valuation",
        "deploymentType": "TFServing",
        "instanceCount": 666,
        "modelId": u"some_model_id",
        "cluster": "some_cluster_id",
    }
    TAGS_JSON = {
        "entity": "deployment",
        "entityId": "sadkfhlskdjh",
        "tags": ["test0", "test1", "test2", "test3"]
    }
    ALL_OPTIONS_REQUEST = {
        "machineType": u"G1",
        "name": u"some_name",
        "imageUrl": u"https://www.latlmes.com/breaking/paperspace-now-has-a-100-bilion-valuation",
        "deploymentType": "TFServing",
        "instanceCount": 666,
        "command": "some deployment command",
        "modelId": u"some_model_id",
        "cluster": "some_cluster_id",
        "containerModelPath": "some/container/model/path",
        "imageUsername": "some_image_username",
        "imagePassword": "some_image_password",
        "imageServer": "some.image/server",
        "containerUrlPath": "some/container/url/path",
        "method": "some_method",
        "dockerArgs": ["some", "docker", "args"],
        "env": {"key": "value"},
        "apiType": "REST",
        "ports": "5000,6000:7000",
        "oauthKey": "some_username",
        "oauthSecret": "some_password",
        "workspaceUrl": u"s3://some-workspace",
        "workspaceRef": "some_branch_name",
        "workspaceUsername": u"username",
        "workspacePassword": u"password",
        "projectId": "some_project_id",
    }
    BASIC_OPTIONS_COMMAND_WITH_AUTOSCALING_REQUEST = {
        "machineType": u"G1",
        "name": u"some_name",
        "imageUrl": u"https://www.latlmes.com/breaking/paperspace-now-has-a-100-bilion-valuation",
        "deploymentType": "TFServing",
        "instanceCount": 666,
        "modelId": u"some_model_id",
        "autoscaling": {
            "minInstanceCount": 4,
            "maxInstanceCount": 64,
            "scaleCooldownPeriod": 123,
            "metrics": [
                {
                    "type": "Resource",
                    "name": "cpu",
                    "valueType": "targetAverage",
                    "value": 10,
                },
                {
                    "type": "Metric",
                    "name": "loss",
                    "valueType": "target",
                    "value": 2.0,
                },
                {
                    "type": "Metric",
                    "name": "keton",
                    "valueType": "target",
                    "value": 21.37,
                },
            ],
        },
    }

    RESPONSE_JSON_200 = example_responses.CREATE_DEPLOYMENT_WITH_BASIC_OPTIONS_RESPONSE
    UPDATE_TAGS_RESPONSE_JSON_200 = example_responses.UPDATE_TAGS_RESPONSE
    EXPECTED_STDOUT = "New deployment created with id: sadkfhlskdjh\n" \
                      "https://console.paperspace.com/deployments/sadkfhlskdjh\n"

    EXPECTED_STDOUT_WITH_WORKSPACE_ARCHIVING = "Archiving your working directory for upload as your experiment workspace..." \
                                               "(See https://docs.paperspace.com/gradient/experiments/run-experiments for more information.)\n" \
                                               "New deployment created with id: sadkfhlskdjh\n" \
                                               "https://console.paperspace.com/deployments/sadkfhlskdjh\n"

    RESPONSE_JSON_404_MODEL_NOT_FOUND = {"error": {"name": "Error", "status": 404, "message": "Unable to find model"}}
    RESPONSE_CONTENT_404_MODEL_NOT_FOUND = b'{"error":{"name":"Error","status":404,"message":"Unable to find model"}}\n'
    EXPECTED_STDOUT_MODEL_NOT_FOUND = "Failed to create resource: Unable to find model\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_deployment_with_basic_options(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.workspace.utils.PathParser.is_local_zip_file", return_value=True)
    @mock.patch("gradient.api_sdk.workspace.tempfile")
    @mock.patch("gradient.api_sdk.s3_uploader.S3FileUploader.upload")
    def test_should_send_proper_data_and_print_message_when_create_deployment_with_zipped_workspace_upload(self,
                                                                                                           mock_upload,
                                                                                                           mock_tempfile,
                                                                                                           mock_parse_path,
                                                                                                           get_patched,
                                                                                                           post_patched):
        bucket_name = "some-bucket"
        team_handle = "thandle"
        archive_location = '/path/to'
        archive_name = "existing_workspace.zip"
        workspace_path = '{}/{}'.format(archive_location, archive_name)
        uuid = 111
        content_type = "application/zip"
        presigned_url = "https://{bucket_name}.s3.amazonaws.com/{team_handle}/deployments/{uuid}/{archive_name}?AWSAccessKeyId=AWSKEY&Content-Type={content_type}&Expires=0&Signature=bar".format(
            bucket_name=bucket_name,
            team_handle=team_handle,
            uuid=uuid,
            archive_name=archive_name,
            content_type=content_type
        )
        workspace_url = "s3://{bucket_name}/{team_handle}/deployments/{uuid}/{archive_name}".format(
            bucket_name=bucket_name,
            team_handle=team_handle,
            uuid=uuid,
            archive_name=archive_name
        )
        presigned_url_return_value = {
            "presignedUrl": presigned_url,
            "bucketName": bucket_name,
            "workspaceUrl": workspace_url
        }
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, "fake content")
        get_patched.return_value = MockResponse(presigned_url_return_value, 200)

        mock_tempfile.gettempdir.return_value = archive_location

        post_params = self.BASIC_OPTIONS_REQUEST.copy()
        post_params['workspaceUrl'] = workspace_url

        cli_command = self.BASIC_OPTIONS_COMMAND + ['--workspace', workspace_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, cli_command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_once_with(self.GET_PRESIGNED_URL,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params={
                                                "contentType": content_type,
                                                "fileName": archive_name,
                                            })
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=post_params,
                                             params=None,
                                             files=None,
                                             data=None)
        mock_upload.assert_called_once_with("{}/{}".format(archive_location, archive_name),
                                            presigned_url)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.workspace.utils.PathParser.parse_path", return_value=utils.PathParser.LOCAL_DIR)
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.workspace.WorkspaceHandler._get_workspace_archiver")
    @mock.patch("gradient.api_sdk.workspace.tempfile")
    @mock.patch("gradient.api_sdk.s3_uploader.S3FileUploader.upload")
    def test_should_send_proper_data_and_print_message_when_create_deployment_with_workspace_zipped_and_uploaded(
            self, mock_upload, mock_tempfile, mock_get_archiver, get_patched, post_patched, _):
        bucket_name = "some-bucket"
        team_handle = "thandle"
        archive_location = '/temp_foo'
        archive_name = "workspace.zip"
        uuid = 111
        content_type = "application/zip"
        presigned_url = "https://{bucket_name}.s3.amazonaws.com/{team_handle}/deployments/{uuid}/{archive_name}?AWSAccessKeyId=AWSKEY&Content-Type={content_type}&Expires=0&Signature=bar".format(
            bucket_name=bucket_name,
            team_handle=team_handle,
            uuid=uuid,
            archive_name=archive_name,
            content_type=content_type
        )
        workspace_url = "s3://{bucket_name}/{team_handle}/deployments/{uuid}/{archive_name}".format(
            bucket_name=bucket_name,
            team_handle=team_handle,
            uuid=uuid,
            archive_name=archive_name
        )
        presigned_url_return_value = {
            "presignedUrl": presigned_url,
            "bucketName": bucket_name,
            "workspaceUrl": workspace_url
        }
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, "fake content")
        get_patched.return_value = MockResponse(presigned_url_return_value, 200)

        mocked_archiver = mock.MagicMock()
        mock_get_archiver.return_value = mocked_archiver
        mock_tempfile.gettempdir.return_value = archive_location

        post_params = self.BASIC_OPTIONS_REQUEST.copy()
        post_params['workspaceUrl'] = workspace_url

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND_WITH_CURRENT_DIR_AS_WORKSPACE)

        assert result.output == self.EXPECTED_STDOUT_WITH_WORKSPACE_ARCHIVING, result.exc_info
        mocked_archiver.archive.assert_called()
        get_patched.assert_called_once_with(self.GET_PRESIGNED_URL,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params={
                                                "contentType": content_type,
                                                "fileName": archive_name,
                                            })
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=post_params,
                                             params=None,
                                             files=None,
                                             data=None)
        mock_upload.assert_called_once_with("{}/{}".format(archive_location, archive_name),
                                            presigned_url)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_request_to_api_v2_when_cluster_id_was_set(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND_WITH_CLUSTER_ID)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST_WHEN_CLUSTER_ID_WAS_SET,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_deployment_with_all_options(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_ALL_OPTIONS)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.ALL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_different_api_key_when_api_key_parameter_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND_WITH_API_KEY)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, post_patched, deployments_create_config_path):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [deployments_create_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.ALL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_wrong_model_id_was_given(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_404_MODEL_NOT_FOUND, 404,
                                                 self.RESPONSE_CONTENT_404_MODEL_NOT_FOUND)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.output == self.EXPECTED_STDOUT_MODEL_NOT_FOUND
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_tag_deployment(self, post_patched, get_patched, put_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, "fake content")
        get_patched.return_value = MockResponse({}, 200, "fake content")
        put_patched.return_value = MockResponse(self.UPDATE_TAGS_RESPONSE_JSON_200, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND_WITH_TAGS)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST,
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

        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_autoscaling_options_with_metric_and_resource_requirements(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND_WITH_AUTOSCALING)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_COMMAND_WITH_AUTOSCALING_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0


class TestDeploymentsList(object):
    URL = "https://api.paperspace.io/deployments/getDeploymentList/"

    COMMAND = ["deployments", "list"]
    COMMAND_WITH_OPTIONS_FILE = ["deployments", "list", "--optionsFile", ]  # path added in test
    LIST_JSON = example_responses.LIST_DEPLOYMENTS

    COMMAND_WITH_API_KEY = ["deployments", "list", "--apiKey", "some_key"]

    COMMAND_WITH_FILTER_WITH_STATE = ["deployments", "list", "--state", "Stopped"]
    LIST_WITH_FILTER_REQUEST_JSON = {"filter": {"where": {"and": [{"state": "Stopped"}]}}}
    LIST_WITH_ALL_FILTERS_REQUEST_JSON = {
        "filter": {
            "where": {
                "and": [
                    {
                        "state": "Building",
                        "projectId": "some_project_id",
                        "modelId": "some_model_id",
                    },
                ],
            },
        },
        "tagFilter": ("some_tag",)
    }
    LIST_WITH_FILTER_RESPONSE_JSON_WHEN_NO_DEPLOYMENTS_FOUND = {"deploymentList": [], "total": 17, "displayTotal": 0,
                                                                "runningTotal": 0}
    DETAILS_STDOUT = """+-----------+-----------------+----------------------------------------------------------------------------------+---------------+-----------------+------------------+
| Name      | ID              | Endpoint                                                                         | Api Type      | Deployment Type | Deployment State |
+-----------+-----------------+----------------------------------------------------------------------------------+---------------+-----------------+------------------+
| some_name | dev61ity7lx232  | https://development-services.paperspace.io/model-serving/dev61ity7lx232:predict  | some_api_type | TFServing       | Stopped          |
| some_name | desanw1jptk7woh | https://development-services.paperspace.io/model-serving/desanw1jptk7woh:predict | REST          | TFServing       | Stopped          |
| some_name | desfnnrqt1v633v | https://development-services.paperspace.io/model-serving/desfnnrqt1v633v:predict | REST          | TFServing       | Stopped          |
| some_name | desdyn55d2e02su | https://development-services.paperspace.io/model-serving/desdyn55d2e02su:predict | REST          | TFServing       | Stopped          |
| some_name | des3tmqa3s627o9 | https://development-services.paperspace.io/model-serving/des3tmqa3s627o9:predict | REST          | TFServing       | Stopped          |
+-----------+-----------------+----------------------------------------------------------------------------------+---------------+-----------------+------------------+
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_list_of_deployments(self, get_patched):
        get_patched.return_value = MockResponse(self.LIST_JSON, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.DETAILS_STDOUT, result.exc_info
        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_with_custom_api_key_when_api_key_parameter_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(self.LIST_JSON, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=None)
        assert result.output == self.DETAILS_STDOUT

    @mock.patch("gradient.cli.deployments.deployments_commands.pydoc")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
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

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_list_of_deployments_filtered_by_state(self, get_patched):
        get_patched.return_value = MockResponse(self.LIST_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_FILTER_WITH_STATE)

        get_patched.assert_called_with("https://api.paperspace.io/deployments/getDeploymentList/",
                                       headers=EXPECTED_HEADERS,
                                       json=self.LIST_WITH_FILTER_REQUEST_JSON,
                                       params=None)
        assert result.output == self.DETAILS_STDOUT

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, get_patched, deployments_list_config_path):
        get_patched.return_value = MockResponse(self.LIST_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [deployments_list_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        get_patched.assert_called_with("https://api.paperspace.io/deployments/getDeploymentList/",
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=self.LIST_WITH_ALL_FILTERS_REQUEST_JSON,
                                       params=None)
        assert result.output == self.DETAILS_STDOUT

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
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
        assert result.output == "No data found\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse({"status": 400, "message": "Invalid API token"},
                                                400)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None)
        assert result.output == "Failed to fetch data: Invalid API token\n", result.exc_info


class TestStartDeployment(object):
    URL_V2 = "https://api.paperspace.io/deployments/v2/updateDeployment/"
    COMMAND = ["deployments", "start",
               "--id", "some_id"]
    COMMAND_WITH_OPTIONS_FILE = ["deployments", "start", "--optionsFile", ]  # path added in test
    REQUEST_JSON = {"isRunning": True, "id": u"some_id"}
    EXPECTED_STDOUT = "Deployment started\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_deployments_start_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=204)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS,
                                             json=self.REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_file(self, post_patched, deployments_start_config_path):
        post_patched.return_value = MockResponse(status_code=204)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [deployments_start_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0


class TestStopDeployment(object):
    URL_V2 = "https://api.paperspace.io/deployments/v2/updateDeployment/"
    COMMAND = ["deployments", "stop",
               "--id", "some_id"]
    REQUEST_JSON = {"isRunning": False, "id": u"some_id"}
    EXPECTED_STDOUT = "Deployment stopped\n"

    COMMAND_WITH_API_KEY = [
        "deployments", "stop",
        "--id", "some_id",
        "--apiKey", "some_key",
    ]
    COMMAND_WITH_OPTIONS_FILE = ["deployments", "stop", "--optionsFile", ]  # path added in test

    RESPONSE_JSON_400 = {"error": {"name": "Error", "status": 400, "message": "Unable to access deployment"}}
    EXPECTED_STDOUT_WITH_WRONG_ID = "Unable to stop instance: Unable to access deployment\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_deployments_stop_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=204)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS,
                                             json=self.REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_with_custom_api_key_when_api_key_parameter_was_provided(self, post_patched):
        post_patched.return_value = MockResponse(status_code=204)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_file(self, post_patched, deployments_stop_config_path):
        post_patched.return_value = MockResponse(status_code=204)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [deployments_stop_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_deployments_stop_used_with_wrong_id(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_400, 400, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_ID, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS,
                                             json=self.REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0


class TestDeleteDeployment(object):
    URL_V2 = "https://api.paperspace.io/deployments/v2/deleteDeployment"

    COMMAND = ["deployments", "delete",
               "--id", "some_id"]
    COMMAND_WITH_API_KEY = [
        "deployments", "delete",
        "--id", "some_id",
        "--apiKey", "some_key",
    ]
    COMMAND_WITH_OPTIONS_FILE = ["deployments", "delete", "--optionsFile", ]

    REQUEST_JSON = {
        "id": "some_id",
        "isRunning": False
    }

    EXPECTED_STDOUT = "Deployment deleted\n"

    RESPONSE_JSON_400 = {"error": {"name": "Error", "status": 400, "message": "Unable to access deployment"}}
    EXPECTED_STDOUT_WITH_WRONG_ID = "Failed to delete resource: Unable to access deployment\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_deployments_delete_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=204)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS,
                                             json=self.REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_with_custom_api_key_when_api_key_parameter_was_provided(self, post_patched):
        post_patched.return_value = MockResponse(status_code=204)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_file(self, post_patched, deployments_stop_config_path):
        post_patched.return_value = MockResponse(status_code=204)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [deployments_stop_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_deployments_delete_used_with_wrong_id(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_400, 400, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_ID, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS,
                                             json=self.REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0


class TestDeploymentsUpdate(object):
    URL_V2 = "https://api.paperspace.io/deployments/v2/updateDeployment"

    BASIC_OPTIONS_COMMAND = [
        "deployments", "update",
        "--id", "some_id",
        "--deploymentType", "tfserving",
    ]
    BASIC_OPTIONS_COMMAND_WITH_API_KEY = [
        "deployments", "update",
        "--id", "some_id",
        "--deploymentType", "tfserving",
        "--apiKey", "some_key",
    ]
    COMMAND_WITH_ALL_OPTIONS = [
        "deployments", "update",
        "--id", "some_id",
        "--deploymentType", "tfserving",
        "--projectId", "some_project_id",
        "--modelId", "some_model_id",
        "--name", "some_name",
        "--machineType", "G1",
        "--imageUrl", "https://www.latlmes.com/breaking/paperspace-now-has-a-100-bilion-valuation",
        "--instanceCount", "666",
        "--command", "echo Bazinga!",
        "--containerModelPath", "some/container/model/path",
        "--imageUsername", "some_image_username",
        "--imagePassword", "some_image_password",
        "--imageServer", "some.image/server",
        "--containerUrlPath", "some/container/url/path",
        "--method", "some_method",
        "--dockerArgs", """["some", "docker", "args"]""",
        "--env", """{"key":"value"}""",
        "--apiType", "REST",
        "--ports", "5000",
        "--authUsername", "some_username",
        "--authPassword", "some_password",
        "--clusterId", "some_cluster_id",
        "--apiKey", "some_key",
        "--workspace", "s3://some-workspace",
        "--workspaceRef", "some_branch_name",
        "--workspaceUsername", "username",
        "--workspacePassword", "password",
        "--minInstanceCount", "4",
        "--maxInstanceCount", "64",
        "--scaleCooldownPeriod", "123",
        "--resource", "cpu/targetAverage:10",
        "--metric", "loss/target:2.0",
        "--metric", "keton/target:21.37",
    ]
    COMMAND_WITH_OPTIONS_FILE = ["deployments", "update", "--optionsFile", ]  # path added in test

    BASIC_OPTIONS_REQUEST = {
        "id": "some_id",
        "upd": {
            "deploymentType": "TFServing",
        }
    }
    ALL_OPTIONS_REQUEST = {
        "id": "some_id",
        "upd": {
            "machineType": u"G1",
            "name": u"some_name",
            "imageUrl": u"https://www.latlmes.com/breaking/paperspace-now-has-a-100-bilion-valuation",
            "deploymentType": "TFServing",
            "instanceCount": 666,
            "command": "echo Bazinga!",
            "modelId": u"some_model_id",
            "clusterId": "some_cluster_id",
            "containerModelPath": "some/container/model/path",
            "imageUsername": "some_image_username",
            "imagePassword": "some_image_password",
            "imageServer": "some.image/server",
            "containerUrlPath": "some/container/url/path",
            "method": "some_method",
            "args": ["some", "docker", "args"],
            "env": {"key": "value"},
            "apiType": "REST",
            "ports": "5000",
            "oauthKey": "some_username",
            "oauthSecret": "some_password",
            "workspaceUrl": u"s3://some-workspace",
            "workspaceRef": "some_branch_name",
            "workspaceUsername": u"username",
            "workspacePassword": u"password",
            "projectId": "some_project_id",
            "autoscaling": {
                "minInstanceCount": 4,
                "maxInstanceCount": 64,
                "scaleCooldownPeriod": 123,
                "metrics": [
                    {
                        "type": "Resource",
                        "name": "cpu",
                        "valueType": "targetAverage",
                        "value": 10,
                    },
                    {
                        "type": "Metric",
                        "name": "loss",
                        "valueType": "target",
                        "value": 2.0,
                    },
                    {
                        "type": "Metric",
                        "name": "keton",
                        "valueType": "target",
                        "value": 21.37,
                    },
                ],
            },
        }
    }
    RESPONSE_JSON_200 = example_responses.CREATE_DEPLOYMENT_WITH_BASIC_OPTIONS_RESPONSE
    EXPECTED_STDOUT = "Deployment data updated\n"

    RESPONSE_JSON_404_MODEL_NOT_FOUND = {
        "error": {"name": "Error", "status": 404, "message": "Model with handle some_model_id does not exist"}}
    EXPECTED_STDOUT_MODEL_NOT_FOUND = "Failed to update resource: Model with handle some_model_id does not exist\n"

    VALIDATE_CLUSTER_URL = "https://api.paperspace.io/clusters/getCluster"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_updated_deployment_with_basic_options(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)

        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_updated_deployment_with_all_options(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_ALL_OPTIONS)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.ALL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_different_api_key_when_api_key_parameter_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND_WITH_API_KEY)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, post_patched, deployments_update_config_path):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [deployments_update_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.ALL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_wrong_model_id_was_given(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_404_MODEL_NOT_FOUND, 404)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.output == self.EXPECTED_STDOUT_MODEL_NOT_FOUND
        assert result.exit_code == 0


class TestDeploymentDetails(object):
    URL = "https://api.paperspace.io/deployments/getDeploymentList/"

    COMMAND = ["deployments", "details", "--id", "some_id"]
    COMMAND_WITH_OPTIONS_FILE = ["deployments", "details", "--optionsFile", ]  # path added in test
    LIST_JSON = example_responses.GET_DEPLOYMENT_DETAILS_JSON_RESPONSE

    COMMAND_WITH_API_KEY = ["deployments", "details", "--id", "some_id", "--apiKey", "some_key"]

    LIST_WITH_FILTER_REQUEST_JSON = {"filter": {"where": {"and": [{"id": "some_id"}]}}}
    LIST_WITH_FILTER_RESPONSE_JSON_WHEN_NO_DEPLOYMENTS_FOUND = {"deploymentList": [], "total": 17, "displayTotal": 0,
                                                                "runningTotal": 0}

    RESPONSE_WITH_ERROR_MESSAGE = {"error": {
        "name": "Error",
        "status": 404,
        "message": "Some error message",
        "statusCode": 404,
    }}

    DETAILS_STDOUT = """+-----------------------+-----------------------------------------------------+
| ID                    | some_id                                             |
+-----------------------+-----------------------------------------------------+
| Name                  | some_name                                           |
| State                 | Stopped                                             |
| Machine type          | p3.2xlarge                                          |
| Instance count        | 1                                                   |
| Command               | some deployment command                             |
| Deployment type       | TFServing                                           |
| Model ID              | some_model_id                                       |
| Project ID            | some_project_id                                     |
| Endpoint              | https://paperspace.io/model-serving/some_id:predict |
| API type              | REST                                                |
| Cluster ID            | some_cluster_id                                     |
| Tags                  | tag1, tag2                                          |
| Min Instance Count    | 4                                                   |
| Max Instance Count    | 64                                                  |
| Scale Cooldown Period | 123                                                 |
| Autoscaling Metrics   | cpu/targetAverage:10.0                              |
|                       | loss/target:2.0                                     |
|                       | keton/target:21.37                                  |
+-----------------------+-----------------------------------------------------+
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_details_of_deployment(self, get_patched):
        get_patched.return_value = MockResponse(self.LIST_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.DETAILS_STDOUT, result.exc_info
        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=self.LIST_WITH_FILTER_REQUEST_JSON,
                                            params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_with_custom_api_key_when_api_key_parameter_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(self.LIST_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=self.LIST_WITH_FILTER_REQUEST_JSON,
                                            params=None)
        assert result.output == self.DETAILS_STDOUT

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_details_of_deployment_when_using_config_file(
            self, get_patched, deployments_details_config_path):
        get_patched.return_value = MockResponse(self.LIST_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [deployments_details_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=self.LIST_WITH_FILTER_REQUEST_JSON,
                                            params=None)
        assert result.output == self.DETAILS_STDOUT

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse({"status": 400, "message": "Invalid API token"}, 400)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=self.LIST_WITH_FILTER_REQUEST_JSON,
                                            params=None)
        assert result.output == "Failed to fetch data: Invalid API token\n", result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_proper_message_when_wrong_deployment_id_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.LIST_WITH_FILTER_RESPONSE_JSON_WHEN_NO_DEPLOYMENTS_FOUND)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=self.LIST_WITH_FILTER_REQUEST_JSON,
                                            params=None)
        assert result.output == "Deployment not found\n", result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_proper_message_when_error_status_was_returned_by_api_without_message(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=self.LIST_WITH_FILTER_REQUEST_JSON,
                                            params=None)
        assert result.output == "Failed to fetch data\n", result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_proper_message_when_error_message_was_returned_by_api(self, get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_WITH_ERROR_MESSAGE, status_code=404)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=self.LIST_WITH_FILTER_REQUEST_JSON,
                                            params=None)
        assert result.output == "Failed to fetch data: Some error message\n", result.exc_info


class TestDeploymentsMetricsGetCommand(object):
    GET_DEPLOYMENTS_LIST_URL = "https://api.paperspace.io/deployments/getDeploymentList/"
    GET_METRICS_URL = "https://aws-testing.paperspace.io/metrics/api/v1/range"
    BASIC_OPTIONS_COMMAND = [
        "deployments", "metrics", "get",
        "--id", "dev61ity7lx232",
    ]
    ALL_OPTIONS_COMMAND = [
        "deployments", "metrics", "get",
        "--id", "dev61ity7lx232",
        "--metric", "gpuMemoryFree",
        "--metric", "gpuMemoryUsed",
        "--interval", "20s",
        "--start", "2020-04-01",
        "--end", "2020-04-02 21:37:00",
        "--apiKey", "some_key",
    ]
    FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE = [
        "deployments", "metrics", "get",
        "--optionsFile",  # path added in test,
    ]

    GET_DEPLOYMENTS_LIST_REQUEST_PARAMS = {"filter": {"where": {"and": [{"id": "dev61ity7lx232"}]}}}
    BASIC_COMMAND_GET_METRICS_REQUEST_PARAMS = {
        "start": "2019-04-04T10:53:56Z",
        "handle": "dev61ity7lx232",
        "interval": "30s",
        "charts": "cpuPercentage,memoryUsage",
        "objecttype": "modelDeployment",
    }
    ALL_COMMANDS_GET_METRICS_REQUEST_PARAMS = {
        "start": "2020-04-01T00:00:00Z",
        "handle": "dev61ity7lx232",
        "interval": "20s",
        "charts": "gpuMemoryFree,gpuMemoryUsed",
        "objecttype": "modelDeployment",
        "end": "2020-04-02T21:37:00Z",
    }

    GET_DEPLOYMENTS_RESPONSE_JSON = example_responses.LIST_DEPLOYMENTS
    GET_METRICS_RESPONSE_JSON = example_responses.DEPLOYMENTS_METRICS_GET_RESPONSE

    EXPECTED_STDOUT = """{
  "cpuPercentage": {
    "desgffa3mtgepvm-0": [
      {
        "time_stamp": 1587340800,
        "value": "0.0388702066666724"
      },
      {
        "time_stamp": 1587370800,
        "value": "0.04452898888887249"
      },
      {
        "time_stamp": 1587400800,
        "value": "0.044658617777757724"
      },
      {
        "time_stamp": 1587430800,
        "value": "0.04922275555555997"
      },
      {
        "time_stamp": 1587460800,
        "value": "0.0589409911111084"
      },
      {
        "time_stamp": 1587490800,
        "value": "0.02873176888891117"
      },
      {
        "time_stamp": 1587520800,
        "value": "0.042048226666666876"
      },
      {
        "time_stamp": 1587550800,
        "value": "0.04952780222222625"
      }
    ],
    "desgffa3mtgepvm-1": [
      {
        "time_stamp": 1587340800,
        "value": "0.05044751111111307"
      },
      {
        "time_stamp": 1587370800,
        "value": "0.04381767555555724"
      },
      {
        "time_stamp": 1587400800,
        "value": "0.03436263111110646"
      },
      {
        "time_stamp": 1587430800,
        "value": "0.048889264444432624"
      },
      {
        "time_stamp": 1587460800,
        "value": "0.041525960000020255"
      },
      {
        "time_stamp": 1587490800,
        "value": "0.04574227333332853"
      },
      {
        "time_stamp": 1587520800,
        "value": "0.03383691777780011"
      },
      {
        "time_stamp": 1587550800,
        "value": "0.045942304444426756"
      }
    ]
  },
  "memoryUsage": {
    "desgffa3mtgepvm-0": [
      {
        "time_stamp": 1587340800,
        "value": "34910208"
      },
      {
        "time_stamp": 1587370800,
        "value": "34910208"
      },
      {
        "time_stamp": 1587400800,
        "value": "34914304"
      },
      {
        "time_stamp": 1587430800,
        "value": "34914304"
      },
      {
        "time_stamp": 1587460800,
        "value": "34914304"
      },
      {
        "time_stamp": 1587490800,
        "value": "34914304"
      },
      {
        "time_stamp": 1587520800,
        "value": "34914304"
      },
      {
        "time_stamp": 1587550800,
        "value": "34914304"
      }
    ],
    "desgffa3mtgepvm-1": [
      {
        "time_stamp": 1587340800,
        "value": "35942400"
      },
      {
        "time_stamp": 1587370800,
        "value": "35942400"
      },
      {
        "time_stamp": 1587400800,
        "value": "35942400"
      },
      {
        "time_stamp": 1587430800,
        "value": "35942400"
      },
      {
        "time_stamp": 1587460800,
        "value": "35942400"
      },
      {
        "time_stamp": 1587490800,
        "value": "35942400"
      },
      {
        "time_stamp": 1587520800,
        "value": "35942400"
      },
      {
        "time_stamp": 1587550800,
        "value": "35942400"
      }
    ]
  }
}

"""

    EXPECTED_STDOUT_WHEN_INVALID_API_KEY_WAS_USED = "Failed to fetch data: Incorrect API Key provided\nForbidden\n"
    EXPECTED_STDOUT_WHEN_EXPERIMENT_WAS_NOT_FOUND = "Deployment not found\n"
    EXPECTED_STDOUT_WHEN_EXPERIMENT_WAS_NOT_STARTED = "Model deployment has not started yet\n"
    EXPECTED_STDOUT_WHEN_NO_METRICS_WERE_FOUND = "{}\n"
    EXPECTED_STDOUT_WHEN_ERROR_CODE_WAS_RETURNED_WITHOUT_ERROR_MESSAGE = "Failed to fetch data\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_all_available_metrics_when_metrics_get_command_was_used_with_basic_options(self, get_patched):
        get_patched.side_effect = [
            MockResponse(self.GET_DEPLOYMENTS_RESPONSE_JSON),
            MockResponse(self.GET_METRICS_RESPONSE_JSON),
        ]

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        assert json.loads(result.output.strip()) == json.loads(self.EXPECTED_STDOUT.strip()), \
            str(result.output) + str(result.exc_info)
        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_DEPLOYMENTS_LIST_URL,
                    json=self.GET_DEPLOYMENTS_LIST_REQUEST_PARAMS,
                    params=None,
                    headers=EXPECTED_HEADERS,
                ),
                mock.call(
                    self.GET_METRICS_URL,
                    json=None,
                    params=self.BASIC_COMMAND_GET_METRICS_REQUEST_PARAMS,
                    headers=EXPECTED_HEADERS,
                ),
            ]
        )

        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_metrics_when_metrics_get_command_was_used_with_all_options(self, get_patched):
        get_patched.side_effect = [
            MockResponse(self.GET_DEPLOYMENTS_RESPONSE_JSON),
            MockResponse(self.GET_METRICS_RESPONSE_JSON),
        ]

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        # comparing objects instead of strings because Py2 and Py3 produce slightly different outputs
        assert json.loads(result.output.strip()) == json.loads(self.EXPECTED_STDOUT.strip()), result.exc_info
        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_DEPLOYMENTS_LIST_URL,
                    json=self.GET_DEPLOYMENTS_LIST_REQUEST_PARAMS,
                    params=None,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
                mock.call(
                    self.GET_METRICS_URL,
                    json=None,
                    params=self.ALL_COMMANDS_GET_METRICS_REQUEST_PARAMS,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
            ]
        )

        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_metrics_when_metrics_get_was_executed_and_options_file_was_used(
            self, get_patched, deployments_metrics_get_config_path):
        get_patched.side_effect = [
            MockResponse(self.GET_DEPLOYMENTS_RESPONSE_JSON),
            MockResponse(self.GET_METRICS_RESPONSE_JSON),
        ]
        command = self.FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE[:] + [deployments_metrics_get_config_path]
        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        # comparing objects instead of strings because Py2 and Py3 produce slightly different outputs
        assert json.loads(result.output.strip()) == json.loads(self.EXPECTED_STDOUT.strip()), result.exc_info
        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_DEPLOYMENTS_LIST_URL,
                    json=self.GET_DEPLOYMENTS_LIST_REQUEST_PARAMS,
                    params=None,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
                mock.call(
                    self.GET_METRICS_URL,
                    json=None,
                    params=self.ALL_COMMANDS_GET_METRICS_REQUEST_PARAMS,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
            ]
        )

        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_invalid_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse({"details": "Incorrect API Key provided", "error": "Forbidden"},
                                                status_code=403)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_INVALID_API_KEY_WAS_USED, result.exc_info

        get_patched.assert_called_once_with(
            self.GET_DEPLOYMENTS_LIST_URL,
            json=self.GET_DEPLOYMENTS_LIST_REQUEST_PARAMS,
            params=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_deployment_was_not_found(self, get_patched):
        get_patched.side_effect = [
            MockResponse({"deploymentList": [], "total": 123, "displayTotal": 0, "runningTotal": 6}),
        ]

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_EXPERIMENT_WAS_NOT_FOUND, result.exc_info

        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_DEPLOYMENTS_LIST_URL,
                    json=self.GET_DEPLOYMENTS_LIST_REQUEST_PARAMS,
                    params=None,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
            ]
        )

        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_message_when_was_no_metrics_were_returned(self, get_patched):
        get_patched.side_effect = [
            MockResponse(self.GET_DEPLOYMENTS_RESPONSE_JSON),
            MockResponse(example_responses.EXPERIMENTS_METRICS_GET_RESPONSE_WHEN_NO_DATA_WAS_FOUND),
        ]

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_NO_METRICS_WERE_FOUND, result.exc_info

        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_DEPLOYMENTS_LIST_URL,
                    json=self.GET_DEPLOYMENTS_LIST_REQUEST_PARAMS,
                    params=None,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
                mock.call(
                    self.GET_METRICS_URL,
                    json=None,
                    params=self.ALL_COMMANDS_GET_METRICS_REQUEST_PARAMS,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
            ]
        )

        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_error_code_was_returned_without_error_message(self, get_patched):
        get_patched.side_effect = [
            MockResponse(self.GET_DEPLOYMENTS_RESPONSE_JSON),
            MockResponse(status_code=500),
        ]

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_ERROR_CODE_WAS_RETURNED_WITHOUT_ERROR_MESSAGE, result.exc_info

        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_DEPLOYMENTS_LIST_URL,
                    json=self.GET_DEPLOYMENTS_LIST_REQUEST_PARAMS,
                    params=None,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
                mock.call(
                    self.GET_METRICS_URL,
                    json=None,
                    params=self.ALL_COMMANDS_GET_METRICS_REQUEST_PARAMS,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
            ]
        )

        assert result.exit_code == 0, result.exc_info


class TestDeploymentssMetricsStreamCommand(object):
    LIST_DEPLOYMENTS_URL = "https://api.paperspace.io/deployments/getDeploymentList/"
    GET_METRICS_URL = "https://aws-testing.paperspace.io/metrics/api/v1/stream"
    BASIC_OPTIONS_COMMAND = [
        "deployments", "metrics", "stream",
        "--id", "dev61ity7lx232",
    ]
    ALL_OPTIONS_COMMAND = [
        "deployments", "metrics", "stream",
        "--id", "dev61ity7lx232",
        "--metric", "gpuMemoryFree",
        "--metric", "gpuMemoryUsed",
        "--interval", "20s",
        "--apiKey", "some_key",
    ]
    ALL_OPTIONS_COMMAND_WITH_OPTIONS_FILE = [
        "deployments", "metrics", "stream",
        "--optionsFile",  # path added in test,
    ]

    GET_DEPLOYMENTS_LIST_REQUEST_JSON = {"filter": {"where": {"and": [{"id": "dev61ity7lx232"}]}}}
    BASIC_COMMAND_CHART_DESCRIPTOR = '{"chart_names": ["cpuPercentage", "memoryUsage"], "handles": ["dev61ity7lx232"' \
                                     '], "object_type": "modelDeployment", "poll_interval": "30s"}'

    ALL_COMMANDS_CHART_DESCRIPTOR = '{"chart_names": ["gpuMemoryFree", "gpuMemoryUsed"], "handles": ["dev61ity7lx232' \
                                    '"], "object_type": "modelDeployment", "poll_interval": "20s"}'

    GET_LIST_OF_DEPLOYMENTS_RESPONSE_JSON = example_responses.LIST_DEPLOYMENTS

    EXPECTED_TABLE_1 = """+-------------------+---------------+-------------+
| Pod               | cpuPercentage | memoryUsage |
+-------------------+---------------+-------------+
| desgffa3mtgepvm-0 |               | 34914304    |
| desgffa3mtgepvm-1 |               | 35942400    |
+-------------------+---------------+-------------+"""
    EXPECTED_TABLE_2 = """+-------------------+----------------------+-------------+
| Pod               | cpuPercentage        | memoryUsage |
+-------------------+----------------------+-------------+
| desgffa3mtgepvm-0 | 0.044894188888835944 | 34914304    |
| desgffa3mtgepvm-1 | 0.048185748888916656 | 35942400    |
+-------------------+----------------------+-------------+"""
    EXPECTED_TABLE_3 = """+-------------------+----------------------+-------------+
| Pod               | cpuPercentage        | memoryUsage |
+-------------------+----------------------+-------------+
| desgffa3mtgepvm-0 | 0.044894188888835944 | 34914304    |
| desgffa3mtgepvm-1 | 0.048185748888916656 | 35942400    |
+-------------------+----------------------+-------------+"""

    ALL_OPTIONS_EXPECTED_TABLE_1 = """+-------------------+---------------+---------------+
| Pod               | gpuMemoryFree | gpuMemoryUsed |
+-------------------+---------------+---------------+
| desgffa3mtgepvm-0 |               | 0             |
| desgffa3mtgepvm-1 |               | 0             |
+-------------------+---------------+---------------+"""
    ALL_OPTIONS_EXPECTED_TABLE_2 = """+-------------------+---------------+---------------+
| Pod               | gpuMemoryFree | gpuMemoryUsed |
+-------------------+---------------+---------------+
| desgffa3mtgepvm-0 |               | 321           |
| desgffa3mtgepvm-1 |               | 432           |
+-------------------+---------------+---------------+"""
    ALL_OPTIONS_EXPECTED_TABLE_3 = """+-------------------+---------------+---------------+
| Pod               | gpuMemoryFree | gpuMemoryUsed |
+-------------------+---------------+---------------+
| desgffa3mtgepvm-0 | 1234          | 321           |
| desgffa3mtgepvm-1 | 234           | 432           |
+-------------------+---------------+---------------+"""

    EXPECTED_STDOUT_WHEN_INVALID_API_KEY_WAS_USED = "Failed to fetch data: Incorrect API Key provided\nForbidden\n"
    EXPECTED_STDOUT_WHEN_DEPLOYMENT_WAS_NOT_FOUND = "Deployment not found\n"

    @mock.patch("gradient.commands.common.TerminalPrinter")
    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_all_available_metrics_when_metrics_get_command_was_used_with_basic_options(
            self, get_patched, create_ws_connection_patched, terminal_printer_cls_patched,
            basic_options_metrics_stream_websocket_connection_iterator):
        get_patched.return_value = MockResponse(self.GET_LIST_OF_DEPLOYMENTS_RESPONSE_JSON)

        ws_connection_instance_mock = mock.MagicMock()
        ws_connection_instance_mock.__iter__ = basic_options_metrics_stream_websocket_connection_iterator
        create_ws_connection_patched.return_value = ws_connection_instance_mock

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        terminal_printer_cls_patched().init.assert_called_once()
        terminal_printer_cls_patched().rewrite_screen.assert_has_calls([
            mock.call(self.EXPECTED_TABLE_1),
            mock.call(self.EXPECTED_TABLE_2),
            mock.call(self.EXPECTED_TABLE_3),
        ])
        terminal_printer_cls_patched().cleanup.assert_called_once()

        get_patched.assert_called_once_with(
            self.LIST_DEPLOYMENTS_URL,
            json=self.GET_DEPLOYMENTS_LIST_REQUEST_JSON,
            params=None,
            headers=EXPECTED_HEADERS,
        )
        ws_connection_instance_mock.send.assert_called_once_with(self.BASIC_COMMAND_CHART_DESCRIPTOR)
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.commands.common.TerminalPrinter")
    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_metrics_when_metrics_get_command_was_used_with_all_options(
            self, get_patched, create_ws_connection_patched, terminal_printer_cls_patched,
            all_options_metrics_stream_websocket_connection_iterator):
        get_patched.return_value = MockResponse(self.GET_LIST_OF_DEPLOYMENTS_RESPONSE_JSON)

        ws_connection_instance_mock = mock.MagicMock()
        ws_connection_instance_mock.__iter__ = all_options_metrics_stream_websocket_connection_iterator
        create_ws_connection_patched.return_value = ws_connection_instance_mock

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        terminal_printer_cls_patched().init.assert_called_once()
        terminal_printer_cls_patched().rewrite_screen.assert_has_calls([
            mock.call(self.ALL_OPTIONS_EXPECTED_TABLE_1),
            mock.call(self.ALL_OPTIONS_EXPECTED_TABLE_2),
            mock.call(self.ALL_OPTIONS_EXPECTED_TABLE_3),
        ])
        terminal_printer_cls_patched().cleanup.assert_called_once()

        get_patched.assert_called_once_with(
            self.LIST_DEPLOYMENTS_URL,
            json=self.GET_DEPLOYMENTS_LIST_REQUEST_JSON,
            params=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        ws_connection_instance_mock.send.assert_called_once_with(self.ALL_COMMANDS_CHART_DESCRIPTOR)
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.commands.common.TerminalPrinter")
    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_metrics_when_metrics_get_was_executed_and_options_file_was_used(
            self, get_patched, create_ws_connection_patched, terminal_printer_cls_patched,
            all_options_metrics_stream_websocket_connection_iterator,
            deployments_metrics_stream_config_path):
        get_patched.return_value = MockResponse(self.GET_LIST_OF_DEPLOYMENTS_RESPONSE_JSON)
        ws_connection_instance_mock = mock.MagicMock()
        ws_connection_instance_mock.__iter__ = all_options_metrics_stream_websocket_connection_iterator
        create_ws_connection_patched.return_value = ws_connection_instance_mock

        command = self.ALL_OPTIONS_COMMAND_WITH_OPTIONS_FILE[:] + [deployments_metrics_stream_config_path]
        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        terminal_printer_cls_patched().init.assert_called_once()
        terminal_printer_cls_patched().rewrite_screen.assert_has_calls([
            mock.call(self.ALL_OPTIONS_EXPECTED_TABLE_1),
            mock.call(self.ALL_OPTIONS_EXPECTED_TABLE_2),
            mock.call(self.ALL_OPTIONS_EXPECTED_TABLE_3),
        ])
        terminal_printer_cls_patched().cleanup.assert_called_once()

        get_patched.assert_called_once_with(
            self.LIST_DEPLOYMENTS_URL,
            json=self.GET_DEPLOYMENTS_LIST_REQUEST_JSON,
            params=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        ws_connection_instance_mock.send.assert_called_once_with(self.ALL_COMMANDS_CHART_DESCRIPTOR)
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.commands.common.TerminalPrinter")
    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_invalid_api_key_was_used(
            self, get_patched, create_ws_connection_patched, terminal_printer_cls_patched):
        get_patched.return_value = MockResponse({"status": 400, "message": "Invalid API token"}, 400)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert "Failed to fetch data: Invalid API token\n" == result.output, result.exc_info

        get_patched.assert_called_once_with(
            self.LIST_DEPLOYMENTS_URL,
            json=self.GET_DEPLOYMENTS_LIST_REQUEST_JSON,
            params=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        create_ws_connection_patched.assert_not_called()
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.commands.common.TerminalPrinter")
    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_deployment_was_not_found(
            self, get_patched, create_ws_connection_patched, terminal_printer_cls_patched):
        get_patched.return_value = MockResponse({"deploymentList": []})

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_DEPLOYMENT_WAS_NOT_FOUND, result.exc_info

        get_patched.assert_called_once_with(
            self.LIST_DEPLOYMENTS_URL,
            json=self.GET_DEPLOYMENTS_LIST_REQUEST_JSON,
            params=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        create_ws_connection_patched.assert_not_called()
        assert result.exit_code == 0, result.exc_info


class TestExperimentLogs(object):
    URL = "https://logs.paperspace.io/jobs/logs"
    COMMAND = ["deployments", "logs", "--id", "some_id"]
    COMMAND_WITH_FOLLOW = ["deployments", "logs", "--id", "some_id", "--follow", "True"]
    COMMAND_WITH_OPTIONS_FILE = ["deployments", "logs", "--optionsFile", ]  # path added in test

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_all_received_logs_when_logs_command_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=example_responses.DEPLOYMENTS_LOGS_RESPONSE)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert "line1" in result.output
        # This one checks if trailing \n was removed from log line.
        # There were empty lines printed if log line had a new line character at the end so we rstrip lines now
        assert "|\n|    " not in result.output

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_should_read_options_from_config_file(self, get_patched, deployments_logs_config_path):
        get_patched.return_value = MockResponse(json_data=example_responses.DEPLOYMENTS_LOGS_RESPONSE)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [deployments_logs_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params={"line": 20, "limit": 30, "deploymentId": "some_id"})
        assert "line2" in result.output
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_all_received_logs_when_logs_command_was_used_with_follow_flag(
            self, get_patched):
        get_patched.return_value = MockResponse(json_data=example_responses.DEPLOYMENTS_LOGS_RESPONSE)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_FOLLOW)

        assert "line3" in result.output

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_error_message_when_wrong_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse(content="Authentication failed",
                                                status_code=401)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_FOLLOW)

        assert "Awaiting logs...\nFailed to fetch data: Authentication failed\n" in result.output
