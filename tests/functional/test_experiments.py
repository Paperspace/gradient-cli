import copy
import json
import os
import shutil
import tempfile
import zipfile

import mock
import pytest
from click.testing import CliRunner
from gradient.api_sdk import constants, sdk_exceptions
from gradient.api_sdk.clients import http_client
from gradient.api_sdk.clients.http_client import default_headers
from gradient.api_sdk.validation_messages import EXPERIMENT_MODEL_PATH_VALIDATION_ERROR
from gradient.cli import cli
from tests import example_responses, MockResponse
from tests.unit.test_archiver_class import create_test_dir_tree

EXPECTED_HEADERS = default_headers.copy()
EXPECTED_HEADERS["ps_client_name"] = "gradient-cli"

EXPECTED_HEADERS_WITH_CHANGED_API_KEY = EXPECTED_HEADERS.copy()
EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"


@pytest.fixture
def temporary_directory_for_extracted_files():
    temp_dir_path = os.path.join(tempfile.gettempdir(), "extracted_files")
    shutil.rmtree(temp_dir_path, ignore_errors=True)

    yield temp_dir_path

    shutil.rmtree(temp_dir_path, ignore_errors=True)


@pytest.fixture
def temporary_zip_file_path():
    zip_file_path = os.path.join(tempfile.gettempdir(), "workspace.zip")

    try:
        os.remove(zip_file_path)
    except OSError:
        pass

    yield zip_file_path

    try:
        os.remove(zip_file_path)
    except OSError:
        pass


@pytest.fixture
def basic_options_metrics_stream_websocket_connection_iterator():
    def generator(self):
        yield """{"handle": "esba290c1osdth",
               "object_type": "experiment",
               "chart_name": "memoryUsage",
               "pod_metrics": {"mljob-esba290c1osdth-0-ps": {"time_stamp": 1587640736, "value": "0"},
                               "mljob-esba290c1osdth-1-worker": {"time_stamp": 1587640736, "value": "0"}}}"""
        yield """{"handle": "esba290c1osdth",
               "object_type": "experiment",
               "chart_name": "memoryUsage",
               "pod_metrics": {"mljob-esba290c1osdth-0-ps": {"time_stamp": 1587640738, "value": "0"},
                               "mljob-esba290c1osdth-1-worker": {"time_stamp": 1587640738, "value": "0"}}}"""
        yield """{"handle": "esba290c1osdth",
               "object_type": "experiment",
               "chart_name": "cpuPercentage",
               "pod_metrics": {"mljob-esba290c1osdth-0-ps": {"time_stamp": 1587640958, "value": "0.004048304444444915"},
                               "mljob-esba290c1osdth-0-worker": {"time_stamp": 1587640958,
                                                                 "value": "33.81072210402445"},
                               "mljob-esba290c1osdth-1-worker": {"time_stamp": 1587640958,
                                                                 "value": "62.25938679226199"}}}"""
        yield """{"handle": "esba290c1osdth",
               "object_type": "experiment",
               "chart_name": "memoryUsage",
               "pod_metrics": {"mljob-esba290c1osdth-0-ps": {"time_stamp": 1587640960, "value": "236097536"},
                               "mljob-esba290c1osdth-0-worker": {"time_stamp": 1587640960, "value": "165785600"},
                               "mljob-esba290c1osdth-1-worker": {"time_stamp": 1587640960, "value": "130957312"}}}"""

        raise sdk_exceptions.GradientSdkError("keton")

    return generator


@pytest.fixture
def all_options_metrics_stream_websocket_connection_iterator():
    def generator(self):
        yield """{"handle": "esba290c1osdth",
               "object_type": "experiment",
               "chart_name": "gpuMemoryUsed",
               "pod_metrics": {"mljob-esba290c1osdth-0-ps": {"time_stamp": 1587640736, "value": "0"},
                               "mljob-esba290c1osdth-1-worker": {"time_stamp": 1587640736, "value": "0"}}}"""
        yield """{"handle": "esba290c1osdth",
               "object_type": "experiment",
               "chart_name": "gpuMemoryUsed",
               "pod_metrics": {"mljob-esba290c1osdth-0-ps": {"time_stamp": 1587640738, "value": "0"},
                               "mljob-esba290c1osdth-1-worker": {"time_stamp": 1587640738, "value": "0"}}}"""
        yield """{"handle": "esba290c1osdth",
               "object_type": "experiment",
               "chart_name": "gpuMemoryFree",
               "pod_metrics": {"mljob-esba290c1osdth-0-ps": {"time_stamp": 1587640958, "value": "1234"},
                               "mljob-esba290c1osdth-0-worker": {"time_stamp": 1587640958,
                                                                 "value": "234"},
                               "mljob-esba290c1osdth-1-worker": {"time_stamp": 1587640958,
                                                                 "value": "345"}}}"""
        yield """{"handle": "esba290c1osdth",
               "object_type": "experiment",
               "chart_name": "gpuMemoryUsed",
               "pod_metrics": {"mljob-esba290c1osdth-0-ps": {"time_stamp": 1587640960, "value": "236097536"},
                               "mljob-esba290c1osdth-0-worker": {"time_stamp": 1587640960, "value": "165785600"},
                               "mljob-esba290c1osdth-1-worker": {"time_stamp": 1587640960, "value": "130957312"}}}"""

        raise sdk_exceptions.GradientSdkError("keton")

    return generator


class TestExperimentsCreateSingleNode(object):
    URL = "https://services.paperspace.io/experiments/v1/experiments/"
    URL_V2 = "https://services.paperspace.io/experiments/v2/experiments/"
    BASIC_OPTIONS_COMMAND = [
        "experiments", "create", "singlenode",
        "--projectId", "testHandle",
        "--container", "testContainer",
        "--machineType", "testType",
        "--command", "testCommand",
        "--workspace", "s3://some-workspace",
    ]
    BASIC_OPTIONS_COMMAND_WITH_LOCAL_WORKSPACE = [
        "experiments", "create", "singlenode",
        "--projectId", "testHandle",
        "--container", "testContainer",
        "--machineType", "testType",
        "--command", "testCommand",
        "--workspace",  # local path added in test
    ]
    FULL_OPTIONS_COMMAND = [
        "experiments", "create", "singlenode",
        "--name", "exp1",
        "--ports", "4567",
        "--workspace", "s3://some-workspace",
        "--workspaceRef", "some_branch_name",
        "--workspaceUsername", "username",
        "--workspacePassword", "password",
        "--workingDirectory", "/work/dir/",
        "--artifactDirectory", "/artifact/dir/",
        "--clusterId", "42c",
        "--experimentEnv", '{"key":"val"}',
        "--projectId", "testHandle",
        "--container", "testContainer",
        "--machineType", "testType",
        "--command", "testCommand",
        "--containerUser", "conUser",
        "--registryUsername", "userName",
        "--registryPassword", "passwd",
        "--registryUrl", "registryUrl",
        "--apiKey", "some_key",
        "--modelPath", "some-model-path",
        "--modelType", "some-model-type",
        "--ignoreFiles", "file1,file2",
        "--isPreemptible",
    ]
    FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE = [
        "experiments", "create", "singlenode",
        "--optionsFile",  # path added in test,
    ]
    FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE_AND_SOME_VALUES_OVERWRITTEN_IN_LINE = [
        "experiments", "create", "singlenode",
        "--name", "some_other_name",
        "--optionsFile",  # path added in test,
    ]
    BASIC_OPTIONS_REQUEST = {
        "projectHandle": u"testHandle",
        "container": u"testContainer",
        "machineType": u"testType",
        "command": u"dGVzdENvbW1hbmQ=",
        "experimentTypeId": constants.ExperimentType.SINGLE_NODE,
        "workspaceUrl": u"s3://some-workspace",
    }
    FULL_OPTIONS_REQUEST = {
        "name": u"exp1",
        "ports": "4567",
        "workspaceUrl": u"s3://some-workspace",
        "workspaceRef": "some_branch_name",
        "workspaceUsername": u"username",
        "workspacePassword": u"password",
        "workingDirectory": u"/work/dir/",
        "artifactDirectory": u"/artifact/dir/",
        "clusterId": "42c",
        "experimentEnv": {u"key": u"val"},
        "projectHandle": u"testHandle",
        "container": u"testContainer",
        "machineType": u"testType",
        "command": u"dGVzdENvbW1hbmQ=",
        "containerUser": u"conUser",
        "registryUsername": u"userName",
        "registryPassword": u"passwd",
        "registryUrl": u"registryUrl",
        "experimentTypeId": constants.ExperimentType.SINGLE_NODE,
        "modelPath": "some-model-path",
        "modelType": "some-model-type",
        "isPreemptible": True,
    }
    RESPONSE_JSON_200 = {"handle": "sadkfhlskdjh", "message": "success"}
    EXPECTED_STDOUT = "New experiment created with ID: sadkfhlskdjh\n"

    RESPONSE_JSON_404_PROJECT_NOT_FOUND = {"details": {"handle": "wrong_handle"}, "error": "Project not found"}
    RESPONSE_CONTENT_404_PROJECT_NOT_FOUND = b'{"details":{"handle":"wrong_handle"},"error":"Project not found"}\n'
    EXPECTED_STDOUT_PROJECT_NOT_FOUND = "handle: wrong_handle\nProject not found\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_experiment_was_run_with_basic_options(self,
                                                                                                         post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info

        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_config_file(
            self, post_patched, create_single_node_experiment_config_path):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)
        command = self.FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE[:] + [create_single_node_experiment_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_config_file_and_overwrite_options_with_values_provided_in_terminal(
            self, post_patched, create_single_node_experiment_config_path):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)
        request_json = copy.deepcopy(self.FULL_OPTIONS_REQUEST)
        request_json["name"] = "some_other_name"
        request_json["projectHandle"] = "some_other_project_id"

        command = self.FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE_AND_SOME_VALUES_OVERWRITTEN_IN_LINE[:]
        command = command[:] + [create_single_node_experiment_config_path, "--projectId", "some_other_project_id"]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=request_json,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_experiment_was_run_with_full_options(self,
                                                                                                        post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.FULL_OPTIONS_COMMAND)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0
        assert EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] == "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_wrong_project_id_was_given(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_404_PROJECT_NOT_FOUND, 404,
                                                 self.RESPONSE_CONTENT_404_PROJECT_NOT_FOUND)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert self.EXPECTED_STDOUT_PROJECT_NOT_FOUND in result.output, result.exc_info[1]
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.commands.experiments.TensorboardHandler")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_use_tensorboard_handler_with_true_value_when_tensorboard_option_was_used_without_value(
            self, post_patched, tensorboard_handler_class, get_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)
        get_patched.return_value = MockResponse(example_responses.GET_V1_CLUSTER_DETAILS_RESPONSE)
        command = self.FULL_OPTIONS_COMMAND[:] + ["--tensorboard=some_tensorboard_id"]
        tensorboard_handler = mock.MagicMock()
        tensorboard_handler_class.return_value = tensorboard_handler

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0
        assert EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] == "some_key"

        tensorboard_handler_class.assert_called_once_with("some_key")
        tensorboard_handler.maybe_add_to_tensorboard.assert_called_once_with("some_tensorboard_id", "sadkfhlskdjh")

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.commands.experiments.TensorboardHandler")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_use_tensorboard_handler_with_tb_id_when_tensorboard_option_was_used_with_tb_id(
            self, post_patched, tensorboard_handler_class, get_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)
        get_patched.return_value = MockResponse(example_responses.GET_V1_CLUSTER_DETAILS_RESPONSE)
        command = self.FULL_OPTIONS_COMMAND[:] + ["--tensorboard"]
        tensorboard_handler = mock.MagicMock()
        tensorboard_handler_class.return_value = tensorboard_handler

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0
        assert EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] == "some_key"

        tensorboard_handler_class.assert_called_once_with("some_key")
        tensorboard_handler.maybe_add_to_tensorboard.assert_called_once_with(True, "sadkfhlskdjh")

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.commands.experiments.TensorboardHandler")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_experiment_was_run_with_full_options(
            self, post_patched, tensorboard_handler_class, get_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)
        get_patched.return_value = MockResponse(example_responses.GET_V1_CLUSTER_DETAILS_RESPONSE)
        command = self.FULL_OPTIONS_COMMAND[:] + ["--tensorboard"]
        tensorboard_handler = mock.MagicMock()
        tensorboard_handler_class.return_value = tensorboard_handler

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0
        assert EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] == "some_key"

        tensorboard_handler_class.assert_called_once_with("some_key")
        tensorboard_handler.maybe_add_to_tensorboard.assert_called_once_with(True, "sadkfhlskdjh")

    @mock.patch("gradient.api_sdk.workspace.s3_uploader.MultipartEncoderWithProgressbar")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_zip_and_upload_local_workspace_when_local_path_was_passed_to_workspace_option(
            self, get_patched,
            post_patched,
            multipart_encoder_cls_patched,
            temporary_directory_for_extracted_files,
            temporary_zip_file_path,
    ):
        multipart_encoder_patched = mock.MagicMock()
        multipart_encoder_content_type = mock.MagicMock()
        # multipart_encoder_patched.content_type = multipart_encoder_content_type
        multipart_monitor = mock.MagicMock()
        multipart_monitor.content_type = multipart_encoder_content_type
        multipart_encoder_patched.get_monitor.return_value = multipart_monitor
        multipart_encoder_cls_patched.return_value = multipart_encoder_patched

        headers_for_uploading_to_s3 = {
            "Content-Type": multipart_encoder_content_type
        }

        get_patched.return_value = MockResponse(example_responses.GET_PRESIGNED_URL_FOR_S3_BUCKET_RESPONSE_JSON)
        post_patched.side_effect = [
            MockResponse(status_code=204),
            MockResponse(status_code=201),
        ]

        workspace_path = create_test_dir_tree()
        zip_file_name = os.path.basename(temporary_zip_file_path)
        command = self.BASIC_OPTIONS_COMMAND_WITH_LOCAL_WORKSPACE[:] + [workspace_path]
        create_experiment_request_json = self.BASIC_OPTIONS_REQUEST.copy()
        create_experiment_request_json["workspaceUrl"] = \
            "s3://ps-projects/" + example_responses.GET_PRESIGNED_URL_FOR_S3_BUCKET_RESPONSE_JSON["data"]["fields"][
                "key"]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        # assert self.EXPECTED_STDOUT in result.output, result.exc_info

        with zipfile.ZipFile(temporary_zip_file_path) as zip_handler:
            zip_handler.extractall(temporary_directory_for_extracted_files)

        file1_path = os.path.join(temporary_directory_for_extracted_files, "file1.txt")
        assert os.path.exists(file1_path)
        assert os.path.isfile(file1_path)
        with open(file1_path) as h:
            assert h.read() == "keton"

        file2_path = os.path.join(temporary_directory_for_extracted_files, "subdir1", "file2.jpg")
        assert os.path.exists(file2_path)
        assert os.path.isfile(file2_path)
        with open(file2_path) as h:
            assert h.read() == "keton"

        get_patched.assert_called_once_with(
            "https://services.paperspace.io/experiments/v1/workspace/get_presigned_url",
            headers=EXPECTED_HEADERS,
            json=None,
            params={"projectHandle": "testHandle", "workspaceName": zip_file_name},
        )

        post_patched.assert_has_calls(
            [
                mock.call(
                    "https://ps-projects.s3.amazonaws.com/",
                    json=None,
                    params=None,
                    headers=headers_for_uploading_to_s3,
                    files=None,
                    data=multipart_monitor,
                ),
                mock.call(
                    self.URL,
                    json=create_experiment_request_json,
                    params=None,
                    headers=EXPECTED_HEADERS,
                    files=None,
                    data=None,
                ),
            ]
        )

        assert result.exit_code == 0


class TestExperimentsCreateMultiNode(object):
    URL = "https://services.paperspace.io/experiments/v1/experiments/"
    URL_V2 = "https://services.paperspace.io/experiments/v2/experiments/"
    BASIC_OPTIONS_COMMAND = [
        "experiments", "create", "multinode",
        "--projectId", "prq70zy79",
        "--experimentType", "GRPC",
        "--workerContainer", "wcon",
        "--workerMachineType", "mty",
        "--workerCommand", "wcom",
        "--workerCount", 2,
        "--parameterServerContainer", "pscon",
        "--parameterServerMachineType", "psmtype",
        "--parameterServerCommand", "ls",
        "--parameterServerCount", 2,
        "--workerContainerUser", "usr",
        "--workspace", "https://github.com/Paperspace/gradient-cli.git",
    ]
    FULL_OPTIONS_COMMAND = [
        "experiments", "create", "multinode",
        "--name", "multinode_mpi",
        "--ports", 3456,
        "--workspace", "s3://some-workspace",
        "--workspaceRef", "some_branch_name",
        "--workspaceUsername", "username",
        "--workspacePassword", "password",
        "--workingDirectory", "/dir",
        "--artifactDirectory", "/artdir",
        "--clusterId", '2a',
        "--experimentEnv", '{"key":"val"}',
        "--projectId", "prq70zy79",
        "--experimentType", "MPI",
        "--workerContainer", "wcon",
        "--workerMachineType", "mty",
        "--workerCommand", "wcom",
        "--workerCount", 2,
        "--masterContainer", "pscon",
        "--masterMachineType", "psmtype",
        "--masterCommand", "ls",
        "--masterCount", 2,
        "--workerContainerUser", "usr",
        "--workerRegistryUsername", "rusr",
        "--workerRegistryPassword", "rpass",
        "--workerRegistryUrl", "rurl",
        "--masterContainerUser", "pscuser",
        "--masterRegistryUsername", "psrcus",
        "--masterRegistryPassword", "psrpass",
        "--masterRegistryUrl", "psrurl",
        "--apiKey", "some_key",
        "--modelPath", "some-model-path",
        "--modelType", "some-model-type",
        "--ignoreFiles", "file1,file2",
        "--isPreemptible",
        "--datasetUri", "s3://some.dataset/uri",
        "--datasetName", "some dataset name",
        "--datasetAwsAccessKeyId", "none",
        "--datasetAwsSecretAccessKey", "none",
        "--datasetVersionId", "version1",
        "--datasetEtag", "some etag",
        "--datasetUri", "s3://some.other.dataset/uri",
        "--datasetName", "none",
        "--datasetAwsAccessKeyId", "some_other_key_id",
        "--datasetAwsSecretAccessKey", "some_other_secret",
        "--datasetVersionId", "version2",
        "--datasetEtag", "some other etag",
        "--datasetVolumeKind", "dynamic",
        "--datasetVolumeSize", "10Gi",
    ]
    FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE = [
        "experiments", "create", "multinode",
        "--optionsFile",  # path added in test,
    ]
    BASIC_OPTIONS_REQUEST = {
        u"projectHandle": u"prq70zy79",
        u"experimentTypeId": 2,
        u"workerContainer": u"wcon",
        u"workerMachineType": u"mty",
        u"workerCommand": u"d2NvbQ==",
        u"workerCount": 2,
        u"parameterServerContainer": u"pscon",
        u"parameterServerMachineType": u"psmtype",
        u"parameterServerCommand": u"bHM=",
        u"parameterServerCount": 2,
        u"workerContainerUser": u"usr",
        u"workspaceUrl": u"https://github.com/Paperspace/gradient-cli.git",
    }
    FULL_OPTIONS_REQUEST = {
        "name": u"multinode_mpi",
        "ports": "3456",
        "workspaceUrl": u"s3://some-workspace",
        "workspaceRef": "some_branch_name",
        "workspaceUsername": u"username",
        "workspacePassword": u"password",
        "workingDirectory": u"/dir",
        "artifactDirectory": u"/artdir",
        "clusterId": '2a',
        "experimentEnv": {"key": "val"},
        "projectHandle": "prq70zy79",
        "experimentTypeId": 3,
        "workerContainer": u"wcon",
        "workerMachineType": u"mty",
        "workerCommand": u"d2NvbQ==",
        "workerCount": 2,
        "masterContainer": u"pscon",
        "masterMachineType": u"psmtype",
        "masterCommand": u"bHM=",
        "masterCount": 2,
        "workerContainerUser": u"usr",
        "workerRegistryUsername": u"rusr",
        "workerRegistryPassword": u"rpass",
        "workerRegistryUrl": u"rurl",
        "masterContainerUser": u"pscuser",
        "masterRegistryUsername": u"psrcus",
        "masterRegistryPassword": u"psrpass",
        "masterRegistryUrl": u"psrurl",
        "isPreemptible": True,
        "modelPath": "some-model-path",
        "modelType": "some-model-type",
        "datasets": [
            {
                "uri": "s3://some.dataset/uri",
                "name": "some dataset name",
                "etag": "some etag",
                "versionId": "version1",
                "volumeOptions": {
                    "kind": "dynamic",
                    "size": "10Gi",
                },
            },
            {
                "uri": "s3://some.other.dataset/uri",
                "awsAccessKeyId": "some_other_key_id",
                "awsSecretAccessKey": "some_other_secret",
                "etag": "some other etag",
                "versionId": "version2",
            },
        ]
    }
    RESPONSE_JSON_200 = {"handle": "sadkfhlskdjh", "message": "success"}
    RESPONSE_CONTENT_200 = b'{"handle":"sadkfhlskdjh","message":"success"}\n'
    EXPECTED_STDOUT = "New experiment created with ID: sadkfhlskdjh\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_experiment_was_run_with_basic_options(self,
                                                                                                         post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_config_file(
            self, post_patched, create_multi_node_experiment_config_path):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)
        command = self.FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE[:] + [create_multi_node_experiment_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_experiment_was_run_with_full_options(self,
                                                                                                        post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.FULL_OPTIONS_COMMAND)

        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert self.EXPECTED_STDOUT in result.output
        assert result.exit_code == 0

    @mock.patch("gradient.commands.experiments.TensorboardHandler")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_use_tensorboard_handler_with_true_value_when_tensorboard_option_was_used_without_value(
            self, post_patched, tensorboard_handler_class):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)
        command = self.FULL_OPTIONS_COMMAND[:] + ["--tensorboard"]
        tensorboard_handler = mock.MagicMock()
        tensorboard_handler_class.return_value = tensorboard_handler

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0
        assert EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] == "some_key"

        tensorboard_handler_class.assert_called_once_with("some_key")
        tensorboard_handler.maybe_add_to_tensorboard.assert_called_once_with(True, "sadkfhlskdjh")

    @mock.patch("gradient.commands.experiments.TensorboardHandler")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_use_tensorboard_handler_with_tb_id_when_tensorboard_option_was_used_with_tb_id(
            self, post_patched, tensorboard_handler_class):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)
        command = self.FULL_OPTIONS_COMMAND[:] + ["--tensorboard=some_tensorboard_id"]
        tensorboard_handler = mock.MagicMock()
        tensorboard_handler_class.return_value = tensorboard_handler

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0
        assert EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] == "some_key"

        tensorboard_handler_class.assert_called_once_with("some_key")
        tensorboard_handler.maybe_add_to_tensorboard.assert_called_once_with("some_tensorboard_id", "sadkfhlskdjh")


    @mock.patch("gradient.commands.experiments.TensorboardHandler")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_experiment_was_run_with_full_options(
            self, post_patched, tensorboard_handler_class):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)
        command = self.FULL_OPTIONS_COMMAND[:] + ["--tensorboard"]
        tensorboard_handler = mock.MagicMock()
        tensorboard_handler_class.return_value = tensorboard_handler

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0
        assert EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] == "some_key"

        tensorboard_handler_class.assert_called_once_with("some_key")
        tensorboard_handler.maybe_add_to_tensorboard.assert_called_once_with(True, "sadkfhlskdjh")

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_config_file_with_dataset_defined_as_list_of_objects(
            self, post_patched, create_multi_node_experiment_ds_objects_config_path):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)
        command = self.FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE[:] + [create_multi_node_experiment_ds_objects_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0


class TestExperimentsCreateAndStartSingleNode(TestExperimentsCreateSingleNode):
    URL = "https://services.paperspace.io/experiments/v1/experiments/run/"
    URL_V2 = "https://services.paperspace.io/experiments/v2/experiments/run/"
    BASIC_OPTIONS_COMMAND = [
        "experiments", "run", "singlenode",
        "--projectId", "testHandle",
        "--container", "testContainer",
        "--machineType", "testType",
        "--command", "testCommand",
        "--workspace", "s3://some-workspace",
        "--no-logs",
    ]
    BASIC_OPTIONS_COMMAND_WITH_LOCAL_WORKSPACE = [
        "experiments", "run", "singlenode",
        "--projectId", "testHandle",
        "--container", "testContainer",
        "--machineType", "testType",
        "--command", "testCommand",
        "--workspace",  # local path added in test
    ]
    FULL_OPTIONS_COMMAND = [
        "experiments", "run", "singlenode",
        "--name", "exp1",
        "--ports", 4567,
        "--workspace", "s3://some-workspace",
        "--workspaceRef", "some_branch_name",
        "--workspaceUsername", "username",
        "--workspacePassword", "password",
        "--workingDirectory", "/work/dir/",
        "--artifactDirectory", "/artifact/dir/",
        "--clusterId", "42c",
        "--experimentEnv", '{"key":"val"}',
        "--projectId", 987654,
        "--projectId", "testHandle",
        "--container", "testContainer",
        "--machineType", "testType",
        "--command", "testCommand",
        "--containerUser", "conUser",
        "--registryUsername", "userName",
        "--registryPassword", "passwd",
        "--registryUrl", "registryUrl",
        "--apiKey", "some_key",
        "--no-logs",
        "--modelPath", "some-model-path",
        "--modelType", "some-model-type",
        "--ignoreFiles", "file1,file2",
        "--isPreemptible",
    ]
    FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE = [
        "experiments", "run", "singlenode",
        "--optionsFile",  # path added in test,
    ]
    FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE_AND_SOME_VALUES_OVERWRITTEN_IN_LINE = [
        "experiments", "run", "singlenode",
        "--name", "some_other_name",
        "--optionsFile",  # path added in test,
    ]
    EXPECTED_STDOUT = "New experiment created and started with ID: sadkfhlskdjh\n"


class TestExperimentsCreateAndStartMultiNode(TestExperimentsCreateMultiNode):
    URL = "https://services.paperspace.io/experiments/v1/experiments/run/"
    URL_V2 = "https://services.paperspace.io/experiments/v2/experiments/run/"
    BASIC_OPTIONS_COMMAND = [
        "experiments", "run", "multinode",
        "--projectId", "prq70zy79",
        "--experimentType", "GRPC",
        "--workerContainer", "wcon",
        "--workerMachineType", "mty",
        "--workerCommand", "wcom",
        "--workerCount", 2,
        "--parameterServerContainer", "pscon",
        "--parameterServerMachineType", "psmtype",
        "--parameterServerCommand", "ls",
        "--parameterServerCount", 2,
        "--workerContainerUser", "usr",
        "--workspace", "https://github.com/Paperspace/gradient-cli.git",
        "--no-logs",
    ]
    FULL_OPTIONS_COMMAND = [
        "experiments", "run", "multinode",
        "--name", "multinode_mpi",
        "--ports", 3456,
        "--workspace", "s3://some-workspace",
        "--workspaceRef", "some_branch_name",
        "--workspaceUsername", "username",
        "--workspacePassword", "password",
        "--workingDirectory", "/dir",
        "--artifactDirectory", "/artdir",
        "--clusterId", '2a',
        "--experimentEnv", '{"key":"val"}',
        "--projectId", 34,
        "--projectId", "prq70zy79",
        "--experimentType", "MPI",
        "--workerContainer", "wcon",
        "--workerMachineType", "mty",
        "--workerCommand", "wcom",
        "--workerCount", 2,
        "--masterContainer", "pscon",
        "--masterMachineType", "psmtype",
        "--masterCommand", "ls",
        "--masterCount", 2,
        "--workerContainerUser", "usr",
        "--workerRegistryUsername", "rusr",
        "--workerRegistryPassword", "rpass",
        "--workerRegistryUrl", "rurl",
        "--masterContainerUser", "pscuser",
        "--masterRegistryUsername", "psrcus",
        "--masterRegistryPassword", "psrpass",
        "--masterRegistryUrl", "psrurl",
        "--apiKey", "some_key",
        "--no-logs",
        "--modelPath", "some-model-path",
        "--modelType", "some-model-type",
        "--ignoreFiles", "file1,file2",
        "--isPreemptible",
        "--datasetUri", "s3://some.dataset/uri",
        "--datasetName", "some dataset name",
        "--datasetAwsAccessKeyId", "none",
        "--datasetAwsSecretAccessKey", "none",
        "--datasetVersionId", "version1",
        "--datasetEtag", "some etag",
        "--datasetUri", "s3://some.other.dataset/uri",
        "--datasetName", "none",
        "--datasetAwsAccessKeyId", "some_other_key_id",
        "--datasetAwsSecretAccessKey", "some_other_secret",
        "--datasetVersionId", "version2",
        "--datasetEtag", "some other etag",
        "--datasetVolumeKind", "dynamic",
        "--datasetVolumeSize", "10Gi",
    ]
    FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE = [
        "experiments", "run", "multinode",
        "--no-logs",
        "--optionsFile",  # path added in test
    ]
    BASIC_OPTIONS_COMMAND_WHEN_CLUSTER_ID_WAS_SET = [
        "experiments", "run", "multinode",
        "--projectId", "prq70zy79",
        "--experimentType", "GRPC",
        "--workerContainer", "wcon",
        "--workerMachineType", "mty",
        "--workerCommand", "wcom",
        "--workerCount", 2,
        "--parameterServerContainer", "pscon",
        "--parameterServerMachineType", "psmtype",
        "--parameterServerCommand", "ls",
        "--parameterServerCount", 2,
        "--workerContainerUser", "usr",
        "--workspace", "https://github.com/Paperspace/gradient-cli.git",
        "--no-logs",
        "--clusterId", "some_cluster_id",
    ]
    EXPECTED_STDOUT = "New experiment created and started with ID: sadkfhlskdjh\n"


class TestExperimentDetail(object):
    URL_V2 = "https://services.paperspace.io/experiments/v2/experiments/experiment-id/"

    COMMAND = ["experiments", "details", "--id", "experiment-id"]
    COMMAND_WITH_API_KEY = ["experiments", "details", "--id", "experiment-id", "--apiKey", "some_key"]
    COMMAND_WITH_OPTIONS_FILE = ["experiments", "details", "--optionsFile", ]  # path added in test

    MULTI_NODE_DETAILS_STDOUT = """+---------------------+--------------------------+
| Name                | some_name                |
+---------------------+--------------------------+
| ID                  | emarbao6t6tsn            |
| State               | pending                  |
| Artifact directory  | /some/artifact/directory |
| Cluster ID          | clqr4b0ox                |
| Experiment Env      | {'key': 'value'}         |
| Experiment Type     | MPI multi node           |
| Model Type          | some_type                |
| Model Path          | /some/model/path         |
| Master Command      | None                     |
| Master Container    | None                     |
| Master Count        | None                     |
| Master Machine Type | None                     |
| Ports               | 5000                     |
| Project ID          | pr85u3sfa                |
| Worker Command      | None                     |
| Worker Container    | None                     |
| Worker Count        | None                     |
| Worker Machine Type | None                     |
| Working Directory   | /some/working/directory  |
| Workspace URL       | some.url                 |
| Tags                | tag1, tag2               |
+---------------------+--------------------------+
"""
    SINGLE_NODE_DETAILS_STDOUT = """+---------------------+----------------+
| Name                | dsfads         |
+---------------------+----------------+
| ID                  | esro6mbmiulvbl |
| State               | created        |
| Ports               | 5000           |
| Project ID          | prq70zy79      |
| Worker Command      | sadas          |
| Worker Container    | asd            |
| Worker Machine Type | C2             |
| Working Directory   | None           |
| Workspace URL       | None           |
| Model Type          | None           |
| Model Path          | None           |
| Tags                | tag1, tag2     |
+---------------------+----------------+
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_single_node_experiment_details_in_a_table(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.DETAILS_OF_SINGLE_NODE_EXPERIMENT_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.SINGLE_NODE_DETAILS_STDOUT, result.exc_info
        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

        assert result.exit_code == 0
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_with_api_key_passed_in_terminal(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.DETAILS_OF_SINGLE_NODE_EXPERIMENT_RESPONSE_JSON)
        expected_headers = EXPECTED_HEADERS.copy()
        expected_headers["X-API-Key"] = "some_key"

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        assert result.output == self.SINGLE_NODE_DETAILS_STDOUT, result.exc_info[1]
        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=expected_headers,
                                            json=None,
                                            params=None)

        assert result.exit_code == 0
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_read_options_from_config_file(self, get_patched, experiment_details_config_path):
        get_patched.return_value = MockResponse(example_responses.DETAILS_OF_SINGLE_NODE_EXPERIMENT_RESPONSE_JSON)
        expected_headers = EXPECTED_HEADERS.copy()
        expected_headers["X-API-Key"] = "some_key"
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [experiment_details_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.SINGLE_NODE_DETAILS_STDOUT, result.exc_info[1]
        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=expected_headers,
                                            json=None,
                                            params=None)

        assert result.exit_code == 0
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_multi_node_experiment_details_in_a_table(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.DETAILS_OF_MULTI_NODE_EXPERIMENT_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

        assert result.output.strip() == self.MULTI_NODE_DETAILS_STDOUT.strip(), result.exc_info[1]
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_request_content_when_response_data_was_malformed(self, get_patched):
        get_patched.return_value = MockResponse({}, content="fake content")
        expected_output = "Error parsing response data: fake content\n"

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

        assert result.output == expected_output, result.exc_info[1]
        assert result.exit_code == 0


class TestExperimentList(object):
    URL_V2 = "https://services.paperspace.io/experiments/v2/experiments/"
    COMMAND = ["experiments", "list"]
    COMMAND_WITH_OPTIONS_FILE = ["experiments", "list", "--optionsFile", ]  # path added in test
    LIST_JSON = example_responses.LIST_OF_EXPERIMENTS_RESPONSE_JSON
    DETAILS_STDOUT = """+---------------+---------------+---------+
| Name          | ID            | Status  |
+---------------+---------------+---------+
| dsfads        | ea2lfbbpdyzsq | created |
| dsfads        | em6btk2vtb7it | created |
| multinode_mpi | ew69ls0vy3eto | created |
+---------------+---------------+---------+

Do you want to continue? [y/N]: 
Aborted!
"""
    RESPONSE_JSON_WHEN_WRONG_API_KEY_WAS_USED = {"details": "Incorrect API Key provided", "error": "Forbidden"}
    EXPECTED_STDOUT_WHEN_WRONG_API_KEY_WAS_USED = "Failed to fetch data: Incorrect API Key provided\nForbidden\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_list_of_experiments(self, get_patched):
        get_patched.return_value = MockResponse(self.LIST_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.DETAILS_STDOUT
        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params={"limit": 20, "offset": 0})

        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.commands.common.pydoc")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_paginate_list_when_output_table_len_is_gt_lines_in_terminal(self, get_patched,
                                                                                                     pydoc_patched):
        list_json = {"data": self.LIST_JSON["data"] * 40}
        get_patched.return_value = MockResponse(list_json)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params={"limit": 20, "offset": 0})

        assert result.exit_code == 1

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_list_of_experiments_filtered_with_two_projects(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.LIST_OF_EXPERIMENTS_FILTERED_WITH_TWO_PROJECTS)

        runner = CliRunner()
        result = runner.invoke(cli.cli, ["experiments", "list", "--projectId", "handle1", "-p", "handle2"])

        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params={"limit": 20,
                                                    "offset": 0,
                                                    "projectHandle[0]": u"handle1",
                                                    "projectHandle[1]": u"handle2"})

        assert result.output == example_responses.LIST_OF_EXPERIMENTS_FILTERED_WITH_TWO_PROJECTS_STDOUT

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_list_of_experiments_filtered_with_two_projects_but_none_found(
            self, get_patched):
        get_patched.return_value = MockResponse(example_responses.LIST_OF_EXPERIMENTS_FILTERED_BUT_NONE_FOUND)

        runner = CliRunner()
        result = runner.invoke(cli.cli, ["experiments", "list", "--projectId", "handle1", "-p", "handle2",
                                         "--tag", "some_tag", "--tag", "some_tag_2"])

        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params={"limit": 20,
                                                    "offset": 0,
                                                    "projectHandle[0]": u"handle1",
                                                    "projectHandle[1]": u"handle2",
                                                    "tag": ("some_tag", "some_tag_2"),
                                                    })

        assert result.output == "No data found\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_WRONG_API_KEY_WAS_USED,
                                                status_code=403)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params={"limit": 20, "offset": 0})

        assert result.output == self.EXPECTED_STDOUT_WHEN_WRONG_API_KEY_WAS_USED
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_defined_in_a_config_file(self, get_patched, experiments_list_config_path):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_WRONG_API_KEY_WAS_USED,
                                                status_code=403)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [experiments_list_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        get_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params={"limit": 20,
                                                    "offset": 0,
                                                    "projectHandle[0]": "some_id",
                                                    "projectHandle[1]": "some_id_2",
                                                    "tag": ("some_tag", "some_tag_2"),
                                                    },
                                            )

        assert result.output == self.EXPECTED_STDOUT_WHEN_WRONG_API_KEY_WAS_USED
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"


class TestStartExperiment(object):
    URL_V2 = "https://services.paperspace.io/experiments/v2/experiments/some-id/start/"
    COMMAND = ["experiments", "start", "--id", "some-id"]
    COMMAND_WITH_OPTIONS_FILE = ["experiments", "start", "--optionsFile", ]  # path added in test
    COMMAND_WITH_API_KEY = ["experiments", "start", "--id", "some-id", "--apiKey", "some_key"]
    RESPONSE_JSON = {"message": "success"}
    START_STDOUT = "Experiment started\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_send_put_request_and_print_confirmation(self, put_patched):
        put_patched.return_value = MockResponse(self.RESPONSE_JSON)
        expected_headers = http_client.default_headers.copy()
        expected_headers["X-API-Key"] = "some_key"

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.START_STDOUT, result.exc_info
        put_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None,
                                            data=None,
                                            )

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_send_put_request_with_changed_api_key_when_api_key_option_was_provided(self, put_patched):
        put_patched.return_value = MockResponse(self.RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        assert result.output == self.START_STDOUT
        put_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=None,
                                            data=None,
                                            )

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_read_options_from_config_file(self, put_patched, experiments_start_config_path):
        put_patched.return_value = MockResponse(self.RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [experiments_start_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.START_STDOUT
        put_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=None,
                                            data=None,
                                            )


class TestStopExperiment(object):
    URL_V2 = "https://services.paperspace.io/experiments/v2/experiments/some-id/stop/"
    COMMAND = ["experiments", "stop", "--id", "some-id"]
    COMMAND_WITH_OPTIONS_FILE = ["experiments", "stop", "--optionsFile", ]  # path added in test
    COMMAND_WITH_API_KEY = ["experiments", "stop", "--id", "some-id", "--apiKey", "some_key"]
    RESPONSE_JSON = {"message": "success"}
    EXPECTED_STDOUT = "Experiment stopped\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_send_put_request_and_print_confirmation(self, put_patched):
        put_patched.return_value = MockResponse(self.RESPONSE_JSON)
        expected_headers = http_client.default_headers.copy()
        expected_headers["X-API-Key"] = "some_key"

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        put_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None,
                                            data=None,
                                            )

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_send_put_request_with_changed_api_key_when_api_key_option_was_provided(self, put_patched):
        put_patched.return_value = MockResponse(self.RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        assert result.output == self.EXPECTED_STDOUT
        put_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=None,
                                            data=None,
                                            )

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_read_options_from_config_file(self, put_patched, experiments_stop_config_path):
        put_patched.return_value = MockResponse(self.RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [experiments_stop_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT
        put_patched.assert_called_once_with(self.URL_V2,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=None,
                                            data=None,
                                            )


class TestDeleteExperiment(object):
    URL = "https://services.paperspace.io/experiments/v2/experiments/some-id/"
    COMMAND = ["experiments", "delete", "--id", "some-id"]
    COMMAND_WITH_OPTIONS_FILE = ["experiments", "delete", "--optionsFile", ]  # path added in test
    COMMAND_WITH_API_KEY = ["experiments", "delete", "--id", "some-id", "--apiKey", "some_key"]
    RESPONSE_JSON = {"message": "success"}
    EXPECTED_STDOUT = "Experiment deleted\n"

    NOT_FOUND_JSON_RESPONSE = {"details": "Experiment not found", "error": "Object not found"}
    NOT_FOUND_EXPECTED_STDOUT = "Failed to delete resource: Experiment not found\nObject not found\n"
    INVALID_API_KEY_RESPONSE_JSON = {"details": "Incorrect API Key provided", "error": "Forbidden"}
    INVALID_API_KEY_STDOUT = "Failed to delete resource: Incorrect API Key provided\nForbidden\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.delete")
    def test_should_send_delete_request_and_print_confirmation(self, delete_patched):
        delete_patched.return_value = MockResponse(self.RESPONSE_JSON, 204)
        expected_headers = http_client.default_headers.copy()
        expected_headers["X-API-Key"] = "some_key"

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        delete_patched.assert_called_once_with(self.URL,
                                               headers=EXPECTED_HEADERS,
                                               json=None,
                                               params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.delete")
    def test_should_send_delete_request_with_changed_api_key_when_api_key_option_was_provided(self, delete_patched):
        delete_patched.return_value = MockResponse(self.RESPONSE_JSON, 204)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        assert result.output == self.EXPECTED_STDOUT
        delete_patched.assert_called_once_with(self.URL,
                                               headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                               json=None,
                                               params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.delete")
    def test_should_read_options_from_config_file(self, delete_patched, experiments_delete_config_path):
        delete_patched.return_value = MockResponse(self.RESPONSE_JSON, 204)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [experiments_delete_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT
        delete_patched.assert_called_once_with(self.URL,
                                               headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                               json=None,
                                               params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.delete")
    def test_should_print_proper_message_when_experiment_was_not_found(self, delete_patched):
        delete_patched.return_value = MockResponse(self.NOT_FOUND_JSON_RESPONSE, 404)
        expected_headers = http_client.default_headers.copy()
        expected_headers["X-API-Key"] = "some_key"

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.NOT_FOUND_EXPECTED_STDOUT, result.exc_info
        delete_patched.assert_called_once_with(self.URL,
                                               headers=EXPECTED_HEADERS,
                                               json=None,
                                               params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.delete")
    def test_should_send_print_proper_message_when_wrong_api_key_was_used(self, delete_patched):
        delete_patched.return_value = MockResponse(self.INVALID_API_KEY_RESPONSE_JSON, 403)
        expected_headers = http_client.default_headers.copy()
        expected_headers["X-API-Key"] = "some_key"

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.INVALID_API_KEY_STDOUT, result.exc_info
        delete_patched.assert_called_once_with(self.URL,
                                               headers=EXPECTED_HEADERS,
                                               json=None,
                                               params=None)


class TestExperimentLogs(object):
    URL = "https://logs.paperspace.io/jobs/logs"
    COMMAND = ["experiments", "logs", "--id", "some_id"]
    COMMAND_WITH_FOLLOW = ["experiments", "logs", "--id", "some_id", "--follow", "True"]
    COMMAND_WITH_OPTIONS_FILE = ["experiments", "logs", "--optionsFile", ]  # path added in test

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_all_received_logs_when_logs_command_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=example_responses.LIST_OF_LOGS_FOR_EXPERIMENT)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert "I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA" in result.output
        # This one checks if trailing \n was removed from log line.
        # There were empty lines printed if log line had a new line character at the end so we rstrip lines now
        assert "|\n|    " not in result.output

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_should_read_options_from_config_file(self, get_patched, experiments_logs_config_path):
        get_patched.return_value = MockResponse(json_data=example_responses.LIST_OF_LOGS_FOR_EXPERIMENT)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [experiments_logs_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params={"line": 20, "limit": 30, "experimentId": "some-id"})
        assert "Downloading https://storage.googleapis.com/cvdf-datasets/mnist/t10k-labels" \
               "-idx1-ubyte.gz to /tmp/tmpbrss4txl.gz" in result.output
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_all_received_logs_when_logs_command_was_used_with_follow_flag(
            self, get_patched):
        get_patched.return_value = MockResponse(json_data=example_responses.LIST_OF_LOGS_FOR_EXPERIMENT)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_FOLLOW)

        assert "Downloading https://storage.googleapis.com/cvdf-datasets/mnist/t10k-labels" \
               "-idx1-ubyte.gz to /tmp/tmpbrss4txl.gz" in result.output

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_error_message_when_wrong_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse(content="Authentication failed",
                                                status_code=401)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_FOLLOW)

        assert "Awaiting logs...\nFailed to fetch data: Authentication failed\n" in result.output


class TestExperimentValidation(object):

    @pytest.mark.parametrize(
        "command, expected_message", [
            (
                    [
                        "experiments", "create", "singlenode",
                        "--projectId", "testHandle",
                        "--container", "testContainer",
                        "--machineType", "testType",
                        "--command", "testCommand",
                        "--workspace", "https://github.com/Paperspace/gradient-cli.git",
                        "--modelPath", "some/model/path"
                    ],
                    EXPERIMENT_MODEL_PATH_VALIDATION_ERROR
            ), (
                    [
                        "experiments", "create", "multinode",
                        "--name", "multinode",
                        "--projectId", "prq70zy79",
                        "--experimentType", "GRPC",
                        "--workerContainer", "wcon",
                        "--workerMachineType", "mty",
                        "--workerCommand", "wcom",
                        "--workerCount", 2,
                        "--parameterServerContainer", "pscon",
                        "--parameterServerMachineType", "psmtype",
                        "--parameterServerCommand", "ls",
                        "--parameterServerCount", 2,
                        "--workerContainerUser", "usr",
                        "--workspace", "https://github.com/Paperspace/gradient-cli.git",
                        "--modelPath", "some/model/path"
                    ],
                    EXPERIMENT_MODEL_PATH_VALIDATION_ERROR
            ), (
                    [
                        "experiments", "run", "singlenode",
                        "--projectId", "testHandle",
                        "--container", "testContainer",
                        "--machineType", "testType",
                        "--command", "testCommand",
                        "--workspace", "https://github.com/Paperspace/gradient-cli.git",
                        "--no-logs",
                        "--modelPath", "some/model/path"
                    ],
                    EXPERIMENT_MODEL_PATH_VALIDATION_ERROR
            ), (
                    [
                        "experiments", "run", "multinode",
                        "--projectId", "prq70zy79",
                        "--experimentType", "GRPC",
                        "--workerContainer", "wcon",
                        "--workerMachineType", "mty",
                        "--workerCommand", "wcom",
                        "--workerCount", 2,
                        "--parameterServerContainer", "pscon",
                        "--parameterServerMachineType", "psmtype",
                        "--parameterServerCommand", "ls",
                        "--parameterServerCount", 2,
                        "--workerContainerUser", "usr",
                        "--workspace", "https://github.com/Paperspace/gradient-cli.git",
                        "--no-logs",
                        "--modelPath", "some/model/path"
                    ],
                    EXPERIMENT_MODEL_PATH_VALIDATION_ERROR
            ),
        ]
    )
    def test_experiment_create_argument_validation_error(self, command, expected_message):
        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert expected_message in result.output


class TestExperimentsMetricsGetCommand(object):
    GET_EXPERIMENT_URL = "https://services.paperspace.io/experiments/v2/experiments/esro6mbmiulvbl/"
    LIST_JOBS_URL = "https://api.paperspace.io/jobs/getJobList/"
    GET_METRICS_URL = "https://aws-testing.paperspace.io/metrics/api/v1/range"
    BASIC_OPTIONS_COMMAND = [
        "experiments", "metrics", "get",
        "--id", "esro6mbmiulvbl",
    ]
    ALL_OPTIONS_COMMAND = [
        "experiments", "metrics", "get",
        "--id", "esro6mbmiulvbl",
        "--metric", "gpuMemoryFree",
        "--metric", "gpuMemoryUsed",
        "--interval", "20s",
        "--start", "2020-04-01",
        "--end", "2020-04-02 21:37:00",
        "--apiKey", "some_key",
    ]
    FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE = [
        "experiments", "metrics", "get",
        "--optionsFile",  # path added in test,
    ]

    GET_JOB_LIST_REQUEST_PARAMS = {'filter': '{"filter": {"where": {"experimentId": "esro6mbmiulvbl"}}}'}
    BASIC_COMMAND_GET_METRICS_REQUEST_PARAMS = {
        "start": "2020-04-02T21:37:00Z",
        "handle": "esro6mbmiulvbl",
        "interval": "30s",
        "charts": "cpuPercentage,memoryUsage",
        "objecttype": "experiment",
    }
    ALL_COMMANDS_GET_METRICS_REQUEST_PARAMS = {
        "start": "2020-04-01T00:00:00Z",
        "handle": "esro6mbmiulvbl",
        "interval": "20s",
        "charts": "gpuMemoryFree,gpuMemoryUsed",
        "objecttype": "experiment",
        "end": "2020-04-02T21:37:00Z",
    }

    GET_EXPERIMENT_RESPONSE_JSON = example_responses.DETAILS_OF_SINGLE_NODE_EXPERIMENT_RESPONSE_JSON
    GET_LIST_OF_JOBS_RESPONSE_JSON = example_responses.LIST_JOBS_RESPONSE_JSON
    GET_METRICS_RESPONSE_JSON = example_responses.EXPERIMENTS_METRICS_GET_RESPONSE

    EXPECTED_STDOUT = """{
  "cpuPercentage": {
    "mljob-esro6mbmiulvbl-0-worker": [
      {
        "time_stamp": 1587375065, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587375095, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587375125, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587375155, 
        "value": "0"
      }
    ], 
    "mljob-esro6mbmiulvbl-1-worker": [
      {
        "time_stamp": 1587375065, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587375095, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587375125, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587375155, 
        "value": "0"
      }
    ]
  }, 
  "memoryUsage": {
    "mljob-esro6mbmiulvbl-0-worker": [
      {
        "time_stamp": 1587375005, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587375035, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587375065, 
        "value": "761856"
      }, 
      {
        "time_stamp": 1587375095, 
        "value": "761856"
      }, 
      {
        "time_stamp": 1587375125, 
        "value": "761856"
      }
    ], 
    "mljob-esro6mbmiulvbl-1-worker": [
      {
        "time_stamp": 1587375005, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587375035, 
        "value": "0"
      }, 
      {
        "time_stamp": 1587375065, 
        "value": "761856"
      }, 
      {
        "time_stamp": 1587375095, 
        "value": "761856"
      }, 
      {
        "time_stamp": 1587375125, 
        "value": "761856"
      }
    ]
  }
}
"""

    EXPECTED_STDOUT_WHEN_INVALID_API_KEY_WAS_USED = "Failed to fetch data: Incorrect API Key provided\nForbidden\n"
    EXPECTED_STDOUT_WHEN_EXPERIMENT_WAS_NOT_FOUND = "Failed to fetch data: Experiment not found\nObject not found\n"
    EXPECTED_STDOUT_WHEN_EXPERIMENT_WAS_NOT_STARTED = "Experiment has not started yet\n"
    EXPECTED_STDOUT_WHEN_NO_METRICS_WERE_FOUND = "{}\n"
    EXPECTED_STDOUT_WHEN_ERROR_CODE_WAS_RETURNED_WITHOUT_ERROR_MESSAGE = "Failed to fetch data\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_all_available_metrics_when_metrics_get_command_was_used_with_basic_options(self, get_patched):
        get_patched.side_effect = [
            MockResponse(self.GET_EXPERIMENT_RESPONSE_JSON),
            MockResponse(self.GET_LIST_OF_JOBS_RESPONSE_JSON),
            MockResponse(self.GET_METRICS_RESPONSE_JSON),
        ]

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        assert json.loads(result.output.strip()) == json.loads(self.EXPECTED_STDOUT.strip()), result.exc_info
        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_EXPERIMENT_URL,
                    json=None,
                    params=None,
                    headers=EXPECTED_HEADERS,
                ),
                mock.call(
                    self.LIST_JOBS_URL,
                    json=None,
                    params=self.GET_JOB_LIST_REQUEST_PARAMS,
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
            MockResponse(self.GET_EXPERIMENT_RESPONSE_JSON),
            MockResponse(self.GET_LIST_OF_JOBS_RESPONSE_JSON),
            MockResponse(self.GET_METRICS_RESPONSE_JSON),
        ]

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        # comparing objects instead of strings because Py2 and Py3 produce slightly different outputs
        assert json.loads(result.output.strip()) == json.loads(self.EXPECTED_STDOUT.strip()), result.exc_info
        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_EXPERIMENT_URL,
                    json=None,
                    params=None,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
                mock.call(
                    self.LIST_JOBS_URL,
                    json=None,
                    params=self.GET_JOB_LIST_REQUEST_PARAMS,
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
            self, get_patched, experiments_metrics_get_config_path):
        get_patched.side_effect = [
            MockResponse(self.GET_EXPERIMENT_RESPONSE_JSON),
            MockResponse(self.GET_LIST_OF_JOBS_RESPONSE_JSON),
            MockResponse(self.GET_METRICS_RESPONSE_JSON),
        ]
        command = self.FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE[:] + [experiments_metrics_get_config_path]
        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        # comparing objects instead of strings because Py2 and Py3 produce slightly different outputs
        assert json.loads(result.output.strip()) == json.loads(self.EXPECTED_STDOUT.strip()), result.exc_info
        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_EXPERIMENT_URL,
                    json=None,
                    params=None,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
                mock.call(
                    self.LIST_JOBS_URL,
                    json=None,
                    params=self.GET_JOB_LIST_REQUEST_PARAMS,
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
            self.GET_EXPERIMENT_URL,
            json=None,
            params=None,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_experiment_was_not_found(self, get_patched):
        get_patched.side_effect = [
            MockResponse({"details": "Experiment not found", "error": "Object not found"}, 404),
        ]

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_EXPERIMENT_WAS_NOT_FOUND, result.exc_info

        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_EXPERIMENT_URL,
                    json=None,
                    params=None,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
            ]
        )

        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_experiment_was_not_started_and_no_jobs_were_found(self, get_patched):
        get_patched.side_effect = [
            MockResponse(self.GET_EXPERIMENT_RESPONSE_JSON),
            MockResponse({"jobList": []}),
        ]

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_EXPERIMENT_WAS_NOT_STARTED, result.exc_info

        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_EXPERIMENT_URL,
                    json=None,
                    params=None,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
            ]
        )

        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_message_when_experiment_was_no_metrics_were_returned(self, get_patched):
        get_patched.side_effect = [
            MockResponse(self.GET_EXPERIMENT_RESPONSE_JSON),
            MockResponse(self.GET_LIST_OF_JOBS_RESPONSE_JSON),
            MockResponse(example_responses.EXPERIMENTS_METRICS_GET_RESPONSE_WHEN_NO_DATA_WAS_FOUND),
        ]

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_NO_METRICS_WERE_FOUND, result.exc_info

        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_EXPERIMENT_URL,
                    json=None,
                    params=None,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
                mock.call(
                    self.LIST_JOBS_URL,
                    json=None,
                    params=self.GET_JOB_LIST_REQUEST_PARAMS,
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
            MockResponse(self.GET_EXPERIMENT_RESPONSE_JSON),
            MockResponse(self.GET_LIST_OF_JOBS_RESPONSE_JSON),
            MockResponse(status_code=500),
        ]

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_ERROR_CODE_WAS_RETURNED_WITHOUT_ERROR_MESSAGE, result.exc_info

        get_patched.assert_has_calls(
            [
                mock.call(
                    self.GET_EXPERIMENT_URL,
                    json=None,
                    params=None,
                    headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                ),
                mock.call(
                    self.LIST_JOBS_URL,
                    json=None,
                    params=self.GET_JOB_LIST_REQUEST_PARAMS,
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


class TestExperimentsMetricsStreamCommand(object):
    LIST_JOBS_URL = "https://api.paperspace.io/jobs/getJobList/"
    GET_METRICS_URL = "https://aws-testing.paperspace.io/metrics/api/v1/stream"
    BASIC_OPTIONS_COMMAND = [
        "experiments", "metrics", "stream",
        "--id", "esro6mbmiulvbl",
    ]
    ALL_OPTIONS_COMMAND = [
        "experiments", "metrics", "stream",
        "--id", "esro6mbmiulvbl",
        "--metric", "gpuMemoryFree",
        "--metric", "gpuMemoryUsed",
        "--interval", "20s",
        "--apiKey", "some_key",
    ]
    ALL_OPTIONS_COMMAND_WITH_OPTIONS_FILE = [
        "experiments", "metrics", "stream",
        "--optionsFile",  # path added in test,
    ]

    GET_JOB_LIST_REQUEST_PARAMS = {'filter': '{"filter": {"where": {"experimentId": "esro6mbmiulvbl"}}}'}
    BASIC_COMMAND_CHART_DESCRIPTOR = '{"chart_names": ["cpuPercentage", "memoryUsage"], "handles": ["esro6mbmiulvbl"]' \
                                     ', "object_type": "experiment", "poll_interval": "30s"}'

    ALL_COMMANDS_CHART_DESCRIPTOR = '{"chart_names": ["gpuMemoryFree", "gpuMemoryUsed"], "handles": ["esro6mbmiulvbl"' \
                                    '], "object_type": "experiment", "poll_interval": "20s"}'

    GET_LIST_OF_JOBS_RESPONSE_JSON = example_responses.LIST_JOBS_RESPONSE_JSON

    EXPECTED_TABLE_1 = """+-------------------------------+---------------+-------------+
| Pod                           | cpuPercentage | memoryUsage |
+-------------------------------+---------------+-------------+
| mljob-esba290c1osdth-0-ps     |               | 0           |
| mljob-esba290c1osdth-1-worker |               | 0           |
+-------------------------------+---------------+-------------+
"""
    EXPECTED_TABLE_2 = """+-------------------------------+---------------+-------------+
| Pod                           | cpuPercentage | memoryUsage |
+-------------------------------+---------------+-------------+
| mljob-esba290c1osdth-0-ps     |               | 0           |
| mljob-esba290c1osdth-1-worker |               | 0           |
+-------------------------------+---------------+-------------+
"""
    EXPECTED_TABLE_3 = """+-------------------------------+----------------------+-------------+
| Pod                           | cpuPercentage        | memoryUsage |
+-------------------------------+----------------------+-------------+
| mljob-esba290c1osdth-0-ps     | 0.004048304444444915 | 0           |
| mljob-esba290c1osdth-0-worker | 33.81072210402445    |             |
| mljob-esba290c1osdth-1-worker | 62.25938679226199    | 0           |
+-------------------------------+----------------------+-------------+
"""
    EXPECTED_TABLE_4 = """+-------------------------------+----------------------+-------------+
| Pod                           | cpuPercentage        | memoryUsage |
+-------------------------------+----------------------+-------------+
| mljob-esba290c1osdth-0-ps     | 0.004048304444444915 | 236097536   |
| mljob-esba290c1osdth-0-worker | 33.81072210402445    | 165785600   |
| mljob-esba290c1osdth-1-worker | 62.25938679226199    | 130957312   |
+-------------------------------+----------------------+-------------+
"""

    ALL_OPTIONS_EXPECTED_TABLE_1 = """+-------------------------------+---------------+---------------+
| Pod                           | gpuMemoryFree | gpuMemoryUsed |
+-------------------------------+---------------+---------------+
| mljob-esba290c1osdth-0-ps     |               | 0             |
| mljob-esba290c1osdth-1-worker |               | 0             |
+-------------------------------+---------------+---------------+
"""
    ALL_OPTIONS_EXPECTED_TABLE_2 = """+-------------------------------+---------------+---------------+
| Pod                           | gpuMemoryFree | gpuMemoryUsed |
+-------------------------------+---------------+---------------+
| mljob-esba290c1osdth-0-ps     |               | 0             |
| mljob-esba290c1osdth-1-worker |               | 0             |
+-------------------------------+---------------+---------------+
"""
    ALL_OPTIONS_EXPECTED_TABLE_3 = """+-------------------------------+---------------+---------------+
| Pod                           | gpuMemoryFree | gpuMemoryUsed |
+-------------------------------+---------------+---------------+
| mljob-esba290c1osdth-0-ps     | 1234          | 0             |
| mljob-esba290c1osdth-0-worker | 234           |               |
| mljob-esba290c1osdth-1-worker | 345           | 0             |
+-------------------------------+---------------+---------------+
"""
    ALL_OPTIONS_EXPECTED_TABLE_4 = """+-------------------------------+---------------+---------------+
| Pod                           | gpuMemoryFree | gpuMemoryUsed |
+-------------------------------+---------------+---------------+
| mljob-esba290c1osdth-0-ps     | 1234          | 236097536     |
| mljob-esba290c1osdth-0-worker | 234           | 165785600     |
| mljob-esba290c1osdth-1-worker | 345           | 130957312     |
+-------------------------------+---------------+---------------+
"""

    EXPECTED_STDOUT_WHEN_INVALID_API_KEY_WAS_USED = "Failed to fetch data: Incorrect API Key provided\nForbidden\n"
    EXPECTED_STDOUT_WHEN_EXPERIMENT_WAS_NOT_FOUND = "Experiment has not started yet\n"
    EXPECTED_STDOUT_WHEN_EXPERIMENT_WAS_NOT_STARTED = "Experiment has not started yet\n"
    EXPECTED_STDOUT_WHEN_NO_METRICS_WERE_FOUND = "{}\n"
    EXPECTED_STDOUT_WHEN_ERROR_CODE_WAS_RETURNED_WITHOUT_ERROR_MESSAGE = "Failed to fetch data\n"

    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_all_available_metrics_when_metrics_get_command_was_used_with_basic_options(
            self, get_patched, create_ws_connection_patched,
            basic_options_metrics_stream_websocket_connection_iterator):
        get_patched.return_value = MockResponse(self.GET_LIST_OF_JOBS_RESPONSE_JSON)

        ws_connection_instance_mock = mock.MagicMock()
        ws_connection_instance_mock.__iter__ = basic_options_metrics_stream_websocket_connection_iterator
        create_ws_connection_patched.return_value = ws_connection_instance_mock

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        assert self.EXPECTED_TABLE_1 in result.output, result.exc_info
        assert self.EXPECTED_TABLE_2 in result.output, result.exc_info
        assert self.EXPECTED_TABLE_3 in result.output, result.exc_info
        assert self.EXPECTED_TABLE_4 in result.output, result.exc_info

        get_patched.assert_called_once_with(
            self.LIST_JOBS_URL,
            json=None,
            params=self.GET_JOB_LIST_REQUEST_PARAMS,
            headers=EXPECTED_HEADERS,
        )
        ws_connection_instance_mock.send.assert_called_once_with(self.BASIC_COMMAND_CHART_DESCRIPTOR)
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_metrics_when_metrics_get_command_was_used_with_all_options(
            self, get_patched, create_ws_connection_patched,
            all_options_metrics_stream_websocket_connection_iterator):
        get_patched.return_value = MockResponse(self.GET_LIST_OF_JOBS_RESPONSE_JSON)

        ws_connection_instance_mock = mock.MagicMock()
        ws_connection_instance_mock.__iter__ = all_options_metrics_stream_websocket_connection_iterator
        create_ws_connection_patched.return_value = ws_connection_instance_mock

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert self.ALL_OPTIONS_EXPECTED_TABLE_1 in result.output, result.exc_info
        assert self.ALL_OPTIONS_EXPECTED_TABLE_2 in result.output, result.exc_info
        assert self.ALL_OPTIONS_EXPECTED_TABLE_3 in result.output, result.exc_info
        assert self.ALL_OPTIONS_EXPECTED_TABLE_4 in result.output, result.exc_info

        get_patched.assert_called_once_with(
            self.LIST_JOBS_URL,
            json=None,
            params=self.GET_JOB_LIST_REQUEST_PARAMS,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        ws_connection_instance_mock.send.assert_called_once_with(self.ALL_COMMANDS_CHART_DESCRIPTOR)
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_metrics_when_metrics_get_was_executed_and_options_file_was_used(
            self, get_patched, create_ws_connection_patched,
            all_options_metrics_stream_websocket_connection_iterator,
            experiments_metrics_stream_config_path):
        get_patched.return_value = MockResponse(self.GET_LIST_OF_JOBS_RESPONSE_JSON)
        ws_connection_instance_mock = mock.MagicMock()
        ws_connection_instance_mock.__iter__ = all_options_metrics_stream_websocket_connection_iterator
        create_ws_connection_patched.return_value = ws_connection_instance_mock

        command = self.ALL_OPTIONS_COMMAND_WITH_OPTIONS_FILE[:] + [experiments_metrics_stream_config_path]
        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.ALL_OPTIONS_EXPECTED_TABLE_1 in result.output, result.exc_info
        assert self.ALL_OPTIONS_EXPECTED_TABLE_2 in result.output, result.exc_info
        assert self.ALL_OPTIONS_EXPECTED_TABLE_3 in result.output, result.exc_info
        assert self.ALL_OPTIONS_EXPECTED_TABLE_4 in result.output, result.exc_info

        get_patched.assert_called_once_with(
            self.LIST_JOBS_URL,
            json=None,
            params=self.GET_JOB_LIST_REQUEST_PARAMS,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        ws_connection_instance_mock.send.assert_called_once_with(self.ALL_COMMANDS_CHART_DESCRIPTOR)
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_invalid_api_key_was_used(
            self, get_patched, create_ws_connection_patched):
        get_patched.return_value = MockResponse({"status": 400, "message": "Invalid API token"}, 400)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert "Failed to fetch data: Invalid API token\n" == result.output, result.exc_info

        get_patched.assert_called_once_with(
            self.LIST_JOBS_URL,
            json=None,
            params=self.GET_JOB_LIST_REQUEST_PARAMS,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        create_ws_connection_patched.assert_not_called()
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_experiment_was_not_found(
            self, get_patched, create_ws_connection_patched):
        get_patched.return_value = MockResponse({"jobList": []})

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_EXPERIMENT_WAS_NOT_FOUND, result.exc_info

        get_patched.assert_called_once_with(
            self.LIST_JOBS_URL,
            json=None,
            params=self.GET_JOB_LIST_REQUEST_PARAMS,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        create_ws_connection_patched.assert_not_called()
        assert result.exit_code == 0, result.exc_info

    @mock.patch("gradient.api_sdk.repositories.common.websocket.create_connection")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_experiment_was_not_started_and_no_jobs_were_found(
            self, get_patched, create_ws_connection_patched):
        get_patched.return_value = MockResponse({"jobList": []})

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.ALL_OPTIONS_COMMAND)

        assert result.output == self.EXPECTED_STDOUT_WHEN_EXPERIMENT_WAS_NOT_FOUND, result.exc_info

        get_patched.assert_called_once_with(
            self.LIST_JOBS_URL,
            json=None,
            params=self.GET_JOB_LIST_REQUEST_PARAMS,
            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
        )

        create_ws_connection_patched.assert_not_called()
        assert result.exit_code == 0, result.exc_info
