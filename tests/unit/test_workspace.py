import os

import mock
import pytest

import gradient.api_sdk.utils
import gradient.cliutils
from gradient.api_sdk.workspace import S3WorkspaceHandler
from gradient.cli_constants import CLI_PS_CLIENT_NAME

MOCK_BUCKET_NAME = 'bucket_name'
MOCK_OBJECT_KEY = 'object_key'
mock_upload_data = {
    "bucket_name": MOCK_BUCKET_NAME,
    "fields": {
        "key": MOCK_OBJECT_KEY
    }
}

mock_upload_response = {
    "message": "success",
    "data": mock_upload_data
}


@pytest.fixture
def workspace_handler():
    s3_workspace_handler = S3WorkspaceHandler("some_key", client_name=CLI_PS_CLIENT_NAME)
    s3_workspace_handler._upload = mock.MagicMock(return_value="s3://{}/{}".format(MOCK_BUCKET_NAME, MOCK_OBJECT_KEY))
    return s3_workspace_handler


class TestWorkspace(object):
    @mock.patch("gradient.utils.PathParser.parse_path", return_value=gradient.api_sdk.utils.PathParser.S3_URL)
    @mock.patch("gradient.api_sdk.workspace.S3WorkspaceHandler._upload")
    def test_dont_upload_if_s3_url_provided(self, _, __, workspace_handler):
        workspace_handler._upload = mock.MagicMock()

        workspace_handler.handle({'workspace': 's3://some-path'})

        workspace_handler._upload.assert_not_called()

    def test_zip_files_and_receive_s3_response_when_no_dir_provided(self, workspace_handler):
        archive_name = 'foo.zip'

        workspace_handler._zip_workspace = mock.MagicMock()
        workspace_handler._zip_workspace.return_value = archive_name

        response_url = workspace_handler.handle({"projectHandle": "some_project_id"})

        workspace_handler._zip_workspace.assert_not_called()
        workspace_handler._upload.assert_not_called()
        assert response_url is None

    @mock.patch("gradient.utils.PathParser.is_local_dir", return_value=True)
    def test_zip_files_and_receive_s3_response_when_workspace_dir_provided(self, _, workspace_handler):
        archive_name = 'foo.zip'

        workspace_handler._zip_workspace = mock.MagicMock()
        workspace_handler._zip_workspace.return_value = archive_name

        response_url = workspace_handler.handle({"projectHandle": "some_project_id", "workspace": "foo/bar"})

        workspace_handler._zip_workspace.assert_called_once()
        workspace_handler._upload.assert_called_once()
        workspace_handler._upload.assert_called_with(archive_name, "some_project_id", cluster_id=None)
        assert response_url == 's3://{}/{}'.format(MOCK_BUCKET_NAME, MOCK_OBJECT_KEY)

    @mock.patch("gradient.utils.PathParser.is_local_zip_file", return_value=True)
    def test_dont_zip_files_and_receive_s3_response_when_workspace_archive_provided(self, _, workspace_handler):
        workspace_handler._zip_workspace = mock.MagicMock()

        response_url = workspace_handler.handle({"projectHandle": "some_project_id", "workspace": "foo.zip"})

        workspace_handler._zip_workspace.assert_not_called()
        workspace_handler._upload.assert_called_once()
        workspace_handler._upload.assert_called_with(os.path.abspath('foo.zip'), "some_project_id", cluster_id=None)
        assert response_url == 's3://{}/{}'.format(MOCK_BUCKET_NAME, MOCK_OBJECT_KEY)

    @mock.patch("gradient.utils.PathParser.is_local_zip_file", return_value=True)
    def test_dont_zip_files_and_receive_s3_response_when_workspace_archive_provided_with_workspace(self, _,
                                                                                                   workspace_handler):
        workspace_handler._zip_workspace = mock.MagicMock()

        response_url = workspace_handler.handle({'projectHandle': 'some_project_id', 'workspace': 'foo.zip'})

        workspace_handler._zip_workspace.assert_not_called()
        workspace_handler._upload.assert_called_once()
        workspace_handler._upload.assert_called_with(os.path.abspath('foo.zip'), "some_project_id", cluster_id=None)
        assert response_url == 's3://{}/{}'.format(MOCK_BUCKET_NAME, MOCK_OBJECT_KEY)
