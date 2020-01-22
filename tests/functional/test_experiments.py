import os
import tempfile
import zipfile

import mock
from click.testing import CliRunner

from gradient.api_sdk import constants
from gradient.api_sdk.clients import http_client
from gradient.cli import cli
from tests import example_responses, MockResponse
from tests.unit.test_archiver_class import create_test_dir_tree


class TestExperimentsCreateSingleNode(object):
    URL = "https://services.paperspace.io/experiments/v1/experiments/"
    URL_V2 = "https://services.paperspace.io/experiments/v2/experiments/"
    EXPECTED_HEADERS = http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"
    BASIC_OPTIONS_COMMAND = [
        "experiments", "create", "singlenode",
        "--name", "exp1",
        "--projectId", "testHandle",
        "--container", "testContainer",
        "--machineType", "testType",
        "--command", "testCommand",
        "--workspaceUrl", "some-workspace",
    ]
    BASIC_OPTIONS_COMMAND_WITH_LOCAL_WORKSPACE = [
        "experiments", "create", "singlenode",
        "--name", "exp1",
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
        "--workspaceUrl", "wsp.url",
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
    BASIC_OPTIONS_REQUEST = {
        "name": u"exp1",
        "projectHandle": u"testHandle",
        "container": u"testContainer",
        "machineType": u"testType",
        "command": u"dGVzdENvbW1hbmQ=",
        "experimentTypeId": constants.ExperimentType.SINGLE_NODE,
        "workspaceUrl": u"some-workspace",
    }
    FULL_OPTIONS_REQUEST = {
        "name": u"exp1",
        "ports": "4567",
        "workspaceUrl": u"wsp.url",
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
    BASIC_OPTIONS_COMMAND_WITH_VPC_SWITCH = [
        "experiments", "create", "singlenode",
        "--name", "exp1",
        "--projectId", "testHandle",
        "--container", "testContainer",
        "--machineType", "testType",
        "--command", "testCommand",
        "--workspaceUrl", "some-workspace",
        "--vpc",
    ]
    RESPONSE_JSON_200 = {"handle": "sadkfhlskdjh", "message": "success"}
    RESPONSE_CONTENT_200 = b'{"handle":"sadkfhlskdjh","message":"success"}\n'
    EXPECTED_STDOUT = "New experiment created with ID: sadkfhlskdjh\n"

    RESPONSE_JSON_404_PROJECT_NOT_FOUND = {"details": {"handle": "wrong_handle"}, "error": "Project not found"}
    RESPONSE_CONTENT_404_PROJECT_NOT_FOUND = b'{"details":{"handle":"wrong_handle"},"error":"Project not found"}\n'
    EXPECTED_STDOUT_PROJECT_NOT_FOUND = "handle: wrong_handle\nProject not found\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_experiment_was_run_with_basic_options(self,
                                                                                                         post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, self.RESPONSE_CONTENT_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_config_file(
            self, post_patched, create_single_node_experiment_config_path):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, self.RESPONSE_CONTENT_200)
        command = self.FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE[:] + [create_single_node_experiment_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_data_to_v2_url_when_vpc_switch_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, self.RESPONSE_CONTENT_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND_WITH_VPC_SWITCH)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info

        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_experiment_was_run_with_full_options(self,
                                                                                                        post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, self.RESPONSE_CONTENT_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.FULL_OPTIONS_COMMAND)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        assert self.EXPECTED_STDOUT in result.output
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0
        assert self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] == "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_wrong_project_id_was_given(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_404_PROJECT_NOT_FOUND, 404,
                                                 self.RESPONSE_CONTENT_404_PROJECT_NOT_FOUND)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert self.EXPECTED_STDOUT_PROJECT_NOT_FOUND in result.output, result.exc_info[1]
        assert result.exit_code == 0

    @mock.patch("gradient.commands.experiments.TensorboardHandler")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_use_tensorboard_handler_with_true_value_when_tensorboard_option_was_used_without_value(
            self, post_patched, tensorboard_handler_class):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)
        command = self.FULL_OPTIONS_COMMAND[:] + ["--tensorboard=some_tensorboard_id"]
        tensorboard_handler = mock.MagicMock()
        tensorboard_handler_class.return_value = tensorboard_handler

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0
        assert self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] == "some_key"

        tensorboard_handler_class.assert_called_once_with("some_key")
        tensorboard_handler.maybe_add_to_tensorboard.assert_called_once_with("some_tensorboard_id", "sadkfhlskdjh")

    @mock.patch("gradient.commands.experiments.TensorboardHandler")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_use_tensorboard_handler_with_tb_id_when_tensorboard_option_was_used_with_tb_id(
            self, post_patched, tensorboard_handler_class):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)
        command = self.FULL_OPTIONS_COMMAND[:] + ["--tensorboard"]
        tensorboard_handler = mock.MagicMock()
        tensorboard_handler_class.return_value = tensorboard_handler

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0
        assert self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] == "some_key"

        tensorboard_handler_class.assert_called_once_with("some_key")
        tensorboard_handler.maybe_add_to_tensorboard.assert_called_once_with(True, "sadkfhlskdjh")

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
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0
        assert self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] == "some_key"

        tensorboard_handler_class.assert_called_once_with("some_key")
        tensorboard_handler.maybe_add_to_tensorboard.assert_called_once_with(True, "sadkfhlskdjh")

    @mock.patch("gradient.workspace.s3_uploader.MultipartEncoderWithProgressbar")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_zip_and_upload_local_workspace_when_local_path_was_passed_to_workspace_option(
            self, get_patched, post_patched, multipart_encoder_cls_patched):
        multipart_encoder_patched = mock.MagicMock()
        multipart_encoder_content_type = mock.MagicMock()
        # multipart_encoder_patched.content_type = multipart_encoder_content_type
        multipart_monitor = mock.MagicMock()
        multipart_monitor.content_type = multipart_encoder_content_type
        multipart_encoder_patched.get_monitor.return_value = multipart_monitor
        multipart_encoder_cls_patched.return_value = multipart_encoder_patched

        headers_for_uploading_to_s3 = self.EXPECTED_HEADERS.copy()
        headers_for_uploading_to_s3["Content-Type"] = multipart_encoder_content_type

        get_patched.return_value = MockResponse(example_responses.GET_PRESIGNED_URL_FOR_S3_BUCKET_RESPONSE_JSON)
        post_patched.side_effect = [
            MockResponse(status_code=204),
            MockResponse(status_code=201),
        ]

        workspace_path = create_test_dir_tree()
        zip_file_name = os.path.basename(workspace_path) + ".zip"
        command = self.BASIC_OPTIONS_COMMAND_WITH_LOCAL_WORKSPACE[:] + [workspace_path]
        zip_file_path = os.path.join(tempfile.gettempdir(), zip_file_name)
        temporary_directory_for_extracted_files = os.path.join(tempfile.gettempdir(), "extracted_files")
        create_experiment_request_json = self.BASIC_OPTIONS_REQUEST.copy()
        create_experiment_request_json["workspaceUrl"] = \
            "s3://ps-projects/" + example_responses.GET_PRESIGNED_URL_FOR_S3_BUCKET_RESPONSE_JSON["data"]["fields"][
                "key"]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        # assert self.EXPECTED_STDOUT in result.output, result.exc_info

        with zipfile.ZipFile(zip_file_path) as zip_handler:
            zip_handler.extractall(temporary_directory_for_extracted_files)

        file1_path = os.path.join(temporary_directory_for_extracted_files, "file1")
        assert os.path.exists(file1_path)
        assert os.path.isfile(file1_path)
        with open(file1_path) as h:
            assert h.read() == "keton"

        file2_path = os.path.join(temporary_directory_for_extracted_files, "subdir1", "file2")
        assert os.path.exists(file2_path)
        assert os.path.isfile(file2_path)
        with open(file2_path) as h:
            assert h.read() == "keton"

        get_patched.assert_called_once_with(
            "https://services.paperspace.io/experiments/v1/workspace/get_presigned_url",
            headers=self.EXPECTED_HEADERS,
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
                    headers=self.EXPECTED_HEADERS,
                    files=None,
                    data=None,
                ),
            ]
        )

        assert result.exit_code == 0


class TestExperimentsCreateMultiNode(object):
    URL = "https://services.paperspace.io/experiments/v1/experiments/"
    URL_V2 = "https://services.paperspace.io/experiments/v2/experiments/"
    EXPECTED_HEADERS = http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"
    BASIC_OPTIONS_COMMAND = [
        "experiments", "create", "multinode",
        "--name", "multinode_mpi",
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
        "--workspaceUrl", "wurl",
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
        "--datasetVersionId", "none",
        "--datasetEtag", "some etag",
        "--datasetUri", "s3://some.other.dataset/uri",
        "--datasetName", "none",
        "--datasetAwsAccessKeyId", "some_other_key_id",
        "--datasetAwsSecretAccessKey", "some_other_secret",
        "--datasetVersionId", "none",
        "--datasetEtag", "some other etag",
    ]
    FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE = [
        "experiments", "create", "multinode",
        "--optionsFile",  # path added in test,
    ]
    BASIC_OPTIONS_REQUEST = {
        u"name": u"multinode_mpi",
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
        "workspaceUrl": u"wurl",
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
            },
            {
                "uri": "s3://some.other.dataset/uri",
                "awsAccessKeyId": "some_other_key_id",
                "awsSecretAccessKey": "some_other_secret",
                "etag": "some other etag",
            },
        ]
    }
    RESPONSE_JSON_200 = {"handle": "sadkfhlskdjh", "message": "success"}
    RESPONSE_CONTENT_200 = b'{"handle":"sadkfhlskdjh","message":"success"}\n'
    EXPECTED_STDOUT = "New experiment created with ID: sadkfhlskdjh\n"

    BASIC_OPTIONS_COMMAND_WITH_VPC_SWITCH = [
        "experiments", "create", "multinode",
        "--name", "multinode_mpi",
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
        "--vpc",
    ]

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_experiment_was_run_with_basic_options(self,
                                                                                                         post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, self.RESPONSE_CONTENT_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_config_file(
            self, post_patched, create_multi_node_experiment_config_path):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, self.RESPONSE_CONTENT_200)
        command = self.FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE[:] + [create_multi_node_experiment_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_experiment_was_run_with_full_options(self,
                                                                                                        post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, self.RESPONSE_CONTENT_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.FULL_OPTIONS_COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert self.EXPECTED_STDOUT in result.output
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_data_to_v2_url_when_vpc_switch_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, self.RESPONSE_CONTENT_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND_WITH_VPC_SWITCH)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info

        post_patched.assert_called_once_with(self.URL_V2,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.commands.experiments.TensorboardHandler")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_use_tensorboard_handler_with_true_value_when_tensorboard_option_was_used_without_value(
            self, post_patched, tensorboard_handler_class):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)
        command = self.FULL_OPTIONS_COMMAND[:] + ["--tensorboard=some_tensorboard_id"]
        tensorboard_handler = mock.MagicMock()
        tensorboard_handler_class.return_value = tensorboard_handler

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0
        assert self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] == "some_key"

        tensorboard_handler_class.assert_called_once_with("some_key")
        tensorboard_handler.maybe_add_to_tensorboard.assert_called_once_with("some_tensorboard_id", "sadkfhlskdjh")

    @mock.patch("gradient.commands.experiments.TensorboardHandler")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_use_tensorboard_handler_with_tb_id_when_tensorboard_option_was_used_with_tb_id(
            self, post_patched, tensorboard_handler_class):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200)
        command = self.FULL_OPTIONS_COMMAND[:] + ["--tensorboard"]
        tensorboard_handler = mock.MagicMock()
        tensorboard_handler_class.return_value = tensorboard_handler

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.EXPECTED_STDOUT in result.output, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0
        assert self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] == "some_key"

        tensorboard_handler_class.assert_called_once_with("some_key")
        tensorboard_handler.maybe_add_to_tensorboard.assert_called_once_with(True, "sadkfhlskdjh")

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
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None,
                                             files=None,
                                             data=None)
        assert result.exit_code == 0
        assert self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] == "some_key"

        tensorboard_handler_class.assert_called_once_with("some_key")
        tensorboard_handler.maybe_add_to_tensorboard.assert_called_once_with(True, "sadkfhlskdjh")


class TestExperimentsCreateAndStartSingleNode(TestExperimentsCreateSingleNode):
    URL = "https://services.paperspace.io/experiments/v1/experiments/run/"
    URL_V2 = "https://services.paperspace.io/experiments/v2/experiments/run/"
    BASIC_OPTIONS_COMMAND = [
        "experiments", "run", "singlenode",
        "--name", "exp1",
        "--projectId", "testHandle",
        "--container", "testContainer",
        "--machineType", "testType",
        "--command", "testCommand",
        "--workspaceUrl", "some-workspace",
        "--no-logs",
    ]
    BASIC_OPTIONS_COMMAND_WITH_LOCAL_WORKSPACE = [
        "experiments", "run", "singlenode",
        "--name", "exp1",
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
        "--workspaceUrl", "wsp.url",
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
    BASIC_OPTIONS_COMMAND_WITH_VPC_SWITCH = [
        "experiments", "run", "singlenode",
        "--name", "exp1",
        "--projectId", "testHandle",
        "--container", "testContainer",
        "--machineType", "testType",
        "--command", "testCommand",
        "--workspaceUrl", "some-workspace",
        "--no-logs",
        "--vpc",
    ]
    EXPECTED_STDOUT = "New experiment created and started with ID: sadkfhlskdjh\n"


class TestExperimentsCreateAndStartMultiNode(TestExperimentsCreateMultiNode):
    URL = "https://services.paperspace.io/experiments/v1/experiments/run/"
    URL_V2 = "https://services.paperspace.io/experiments/v2/experiments/run/"
    BASIC_OPTIONS_COMMAND = [
        "experiments", "run", "multinode",
        "--name", "multinode_mpi",
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
        "--workspaceUrl", "wurl",
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
        "--datasetVersionId", "none",
        "--datasetEtag", "some etag",
        "--datasetUri", "s3://some.other.dataset/uri",
        "--datasetName", "none",
        "--datasetAwsAccessKeyId", "some_other_key_id",
        "--datasetAwsSecretAccessKey", "some_other_secret",
        "--datasetVersionId", "none",
        "--datasetEtag", "some other etag",
    ]
    FULL_OPTIONS_COMMAND_WITH_OPTIONS_FILE = [
        "experiments", "run", "multinode",
        "--optionsFile",  # path added in test
    ]
    BASIC_OPTIONS_COMMAND_WITH_VPC_SWITCH = [
        "experiments", "run", "multinode",
        "--name", "multinode_mpi",
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
        "--vpc",
    ]
    EXPECTED_STDOUT = "New experiment created and started with ID: sadkfhlskdjh\n"


class TestExperimentDetail(object):
    URL = "https://services.paperspace.io/experiments/v1/experiments/experiment-id/"
    EXPECTED_HEADERS = http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    COMMAND = ["experiments", "details", "experiment-id"]
    COMMAND_WITH_API_KEY = ["experiments", "details", "experiment-id", "--apiKey", "some_key"]
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
+---------------------+----------------+
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_single_node_experiment_details_in_a_table(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.DETAILS_OF_SINGLE_NODE_EXPERIMENT_RESPONSE_JSON,
                                                200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.SINGLE_NODE_DETAILS_STDOUT, result.exc_info[1]
        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

        assert result.exit_code == 0
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_with_api_key_passed_in_terminal(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.DETAILS_OF_SINGLE_NODE_EXPERIMENT_RESPONSE_JSON,
                                                200, "fake content")
        expected_headers = self.EXPECTED_HEADERS.copy()
        expected_headers["X-API-Key"] = "some_key"

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        assert result.output == self.SINGLE_NODE_DETAILS_STDOUT, result.exc_info[1]
        get_patched.assert_called_once_with(self.URL,
                                            headers=expected_headers,
                                            json=None,
                                            params=None)

        assert result.exit_code == 0
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_read_options_from_config_file(self, get_patched, experiment_details_config_path):
        get_patched.return_value = MockResponse(example_responses.DETAILS_OF_SINGLE_NODE_EXPERIMENT_RESPONSE_JSON,
                                                200, "fake content")
        expected_headers = self.EXPECTED_HEADERS.copy()
        expected_headers["X-API-Key"] = "some_key"
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [experiment_details_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.SINGLE_NODE_DETAILS_STDOUT, result.exc_info[1]
        get_patched.assert_called_once_with(self.URL,
                                            headers=expected_headers,
                                            json=None,
                                            params=None)

        assert result.exit_code == 0
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_multi_node_experiment_details_in_a_table(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.DETAILS_OF_MULTI_NODE_EXPERIMENT_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

        assert result.output.strip() == self.MULTI_NODE_DETAILS_STDOUT.strip(), result.exc_info[1]
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_request_content_when_response_data_was_malformed(self, get_patched):
        get_patched.return_value = MockResponse({}, 200, "fake content")
        expected_output = "Error parsing response data: fake content\n"

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

        assert result.output == expected_output, result.exc_info[1]
        assert result.exit_code == 0


class TestExperimentList(object):
    URL = "https://services.paperspace.io/experiments/v1/experiments/"
    COMMAND = ["experiments", "list"]
    COMMAND_WITH_OPTIONS_FILE = ["experiments", "list", "--optionsFile", ]  # path added in test
    EXPECTED_HEADERS = http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"
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
        get_patched.return_value = MockResponse(self.LIST_JSON, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.DETAILS_STDOUT
        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params={"limit": 20, "offset": 0})

        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.commands.common.pydoc")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_paginate_list_when_output_table_len_is_gt_lines_in_terminal(self, get_patched,
                                                                                                     pydoc_patched):
        list_json = {"data": self.LIST_JSON["data"] * 40}
        get_patched.return_value = MockResponse(list_json, 200, "")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params={"limit": 20, "offset": 0})

        assert result.exit_code == 1

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_list_of_experiments_filtered_with_two_projects(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.LIST_OF_EXPERIMENTS_FILTERED_WITH_TWO_PROJECTS, 200,
                                                "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, ["experiments", "list", "--projectId", "handle1", "-p", "handle2"])

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params={"limit": 20,
                                                    "offset": 0,
                                                    "projectHandle[0]": u"handle1",
                                                    "projectHandle[1]": u"handle2"})

        assert result.output == example_responses.LIST_OF_EXPERIMENTS_FILTERED_WITH_TWO_PROJECTS_STDOUT

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_list_of_experiments_filtered_with_two_projects_but_none_found(
            self, get_patched):
        get_patched.return_value = MockResponse(example_responses.LIST_OF_EXPERIMENTS_FILTERED_BUT_NONE_FOUND, 200,
                                                "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, ["experiments", "list", "--projectId", "handle1", "-p", "handle2"])

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params={"limit": 20,
                                                    "offset": 0,
                                                    "projectHandle[0]": u"handle1",
                                                    "projectHandle[1]": u"handle2"})

        assert result.output == "No data found\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_WRONG_API_KEY_WAS_USED,
                                                status_code=403)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params={"limit": 20, "offset": 0})

        assert result.output == self.EXPECTED_STDOUT_WHEN_WRONG_API_KEY_WAS_USED
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_defined_in_a_config_file(self, get_patched, experiments_list_config_path):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_WRONG_API_KEY_WAS_USED,
                                                status_code=403)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [experiments_list_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params={"limit": 20,
                                                    "offset": 0,
                                                    "projectHandle[0]": "some_id",
                                                    "projectHandle[1]": "some_id_2"})

        assert result.output == self.EXPECTED_STDOUT_WHEN_WRONG_API_KEY_WAS_USED
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"


class TestStartExperiment(object):
    URL = "https://services.paperspace.io/experiments/v1/experiments/some-id/start/"
    URL_V2 = "https://services.paperspace.io/experiments/v2/experiments/some-id/start/"
    COMMAND = ["experiments", "start", "some-id"]
    COMMAND_WITH_OPTIONS_FILE = ["experiments", "start", "--optionsFile", ]  # path added in test
    COMMAND_WITH_VPC_FLAG = ["experiments", "start", "some-id", "--vpc"]
    EXPECTED_HEADERS = http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"
    COMMAND_WITH_API_KEY = ["experiments", "start", "some-id", "--apiKey", "some_key"]
    RESPONSE_JSON = {"message": "success"}
    START_STDOUT = "Experiment started\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_send_put_request_and_print_confirmation(self, put_patched):
        put_patched.return_value = MockResponse(self.RESPONSE_JSON, 200, "fake content")
        expected_headers = http_client.default_headers.copy()
        expected_headers["X-API-Key"] = "some_key"

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.START_STDOUT, result.exc_info
        put_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_send_request_to_api_v2_when_vcp_flag_was_used(self, put_patched):
        put_patched.return_value = MockResponse(self.RESPONSE_JSON, 200, "fake content")
        expected_headers = http_client.default_headers.copy()
        expected_headers["X-API-Key"] = "some_key"

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_VPC_FLAG)

        assert result.output == self.START_STDOUT, result.exc_info
        put_patched.assert_called_once_with(self.URL_V2,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_send_put_request_with_changed_api_key_when_api_key_option_was_provided(self, put_patched):
        put_patched.return_value = MockResponse(self.RESPONSE_JSON, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        assert result.output == self.START_STDOUT
        put_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_read_options_from_config_file(self, put_patched, experiments_start_config_path):
        put_patched.return_value = MockResponse(self.RESPONSE_JSON, 200, "fake content")
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [experiments_start_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.START_STDOUT
        put_patched.assert_called_once_with(self.URL_V2,
                                            headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=None)


class TestStopExperiment(object):
    URL = "https://services.paperspace.io/experiments/v1/experiments/some-id/stop/"
    URL_V2 = "https://services.paperspace.io/experiments/v2/experiments/some-id/stop/"
    COMMAND = ["experiments", "stop", "some-id"]
    COMMAND_WITH_VPC_FLAG = ["experiments", "stop", "some-id", "--vpc"]
    COMMAND_WITH_OPTIONS_FILE = ["experiments", "stop", "--optionsFile", ]  # path added in test
    EXPECTED_HEADERS = http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"
    COMMAND_WITH_API_KEY = ["experiments", "stop", "some-id", "--apiKey", "some_key"]
    RESPONSE_JSON = {"message": "success"}
    EXPECTED_STDOUT = "Experiment stopped\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_send_put_request_and_print_confirmation(self, put_patched):
        put_patched.return_value = MockResponse(self.RESPONSE_JSON, 200, "fake content")
        expected_headers = http_client.default_headers.copy()
        expected_headers["X-API-Key"] = "some_key"

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        put_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_send_request_to_api_v2_when_vcp_flag_was_used(self, put_patched):
        put_patched.return_value = MockResponse(self.RESPONSE_JSON, 200, "fake content")
        expected_headers = http_client.default_headers.copy()
        expected_headers["X-API-Key"] = "some_key"

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_VPC_FLAG)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        put_patched.assert_called_once_with(self.URL_V2,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_send_put_request_with_changed_api_key_when_api_key_option_was_provided(self, put_patched):
        put_patched.return_value = MockResponse(self.RESPONSE_JSON, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        assert result.output == self.EXPECTED_STDOUT
        put_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_read_options_from_config_file(self, put_patched, experiments_stop_config_path):
        put_patched.return_value = MockResponse(self.RESPONSE_JSON, 200, "fake content")
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [experiments_stop_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT
        put_patched.assert_called_once_with(self.URL_V2,
                                            headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=None)


class TestDeleteExperiment(object):
    URL = "https://services.paperspace.io/experiments/v1/experiments/some-id/"
    COMMAND = ["experiments", "delete", "some-id"]
    COMMAND_WITH_OPTIONS_FILE = ["experiments", "delete", "--optionsFile", ]  # path added in test
    EXPECTED_HEADERS = http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"
    COMMAND_WITH_API_KEY = ["experiments", "delete", "some-id", "--apiKey", "some_key"]
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
                                               headers=self.EXPECTED_HEADERS,
                                               json=None,
                                               params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.delete")
    def test_should_send_delete_request_with_changed_api_key_when_api_key_option_was_provided(self, delete_patched):
        delete_patched.return_value = MockResponse(self.RESPONSE_JSON, 204)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        assert result.output == self.EXPECTED_STDOUT
        delete_patched.assert_called_once_with(self.URL,
                                               headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
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
                                               headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
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
                                               headers=self.EXPECTED_HEADERS,
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
                                               headers=self.EXPECTED_HEADERS,
                                               json=None,
                                               params=None)


class TestExperimentLogs(object):
    URL = "https://logs.paperspace.io/jobs/logs"
    COMMAND = ["experiments", "logs", "--experimentId", "some_id"]
    COMMAND_WITH_FOLLOW = ["experiments", "logs", "--experimentId", "some_id", "--follow", "True"]
    COMMAND_WITH_OPTIONS_FILE = ["experiments", "logs", "--optionsFile", ]  # path added in test

    EXPECTED_HEADERS = http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some-key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_all_received_logs_when_logs_command_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=example_responses.LIST_OF_LOGS_FOR_EXPERIMENT,
                                                status_code=200)

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
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params={"line": 20, "limit": 30, "experimentId": "some-id"})
        assert "Downloading https://storage.googleapis.com/cvdf-datasets/mnist/t10k-labels" \
               "-idx1-ubyte.gz to /tmp/tmpbrss4txl.gz" in result.output
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_all_received_logs_when_logs_command_was_used_with_follow_flag(
            self, get_patched):
        get_patched.return_value = MockResponse(json_data=example_responses.LIST_OF_LOGS_FOR_EXPERIMENT,
                                                status_code=200)

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
