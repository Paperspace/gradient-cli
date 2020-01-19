import os

import click
import mock
import pytest

import gradient.utils
from gradient.workspace import S3WorkspaceHandler

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
    s3_workspace_handler = S3WorkspaceHandler("some_key")
    s3_workspace_handler._upload = mock.MagicMock(return_value="s3://{}/{}".format(MOCK_BUCKET_NAME, MOCK_OBJECT_KEY))
    return s3_workspace_handler


class TestWorkspace(object):

    @pytest.mark.parametrize('params', ({'workspace': 'foo', 'workspaceUrl': 'bar'},
                                        {'workspaceUrl': 'ffo', 'workspaceArchive': 'var'},
                                        {'workspaceArchive': 'foo', 'workspace': 'bar'},
                                        {'workspace': 'foo', 'workspaceUrl': 'bar', 'workspaceArchive': 'baz'}))
    def test_raise_exception_when_more_than_one_workspace_provided(self, params):
        workspace_handler = S3WorkspaceHandler(mock.MagicMock, mock.MagicMock)
        with pytest.raises(click.UsageError):
            workspace_handler.handle(params)

    @mock.patch("gradient.utils.PathParser.parse_path", return_value=gradient.utils.PathParser.LOCAL_FILE)
    @mock.patch("gradient.workspace.S3WorkspaceHandler._upload")
    def test_dont_upload_if_archive_path_provided(self, _, __, workspace_handler):
        workspace_handler._upload = mock.MagicMock()

        workspace_handler.handle({'workspaceUrl': 'foo'})

        workspace_handler._upload.assert_not_called()

    @mock.patch("gradient.utils.PathParser.parse_path", return_value=None)
    def test_zip_files_and_receive_s3_response_when_no_dir_provided(self, _, workspace_handler):
        archive_name = 'foo.zip'

        workspace_handler._zip_workspace = mock.MagicMock()
        workspace_handler._zip_workspace.return_value = archive_name

        response_url = workspace_handler.handle({"projectHandle": "some_project_id"})

        workspace_handler._zip_workspace.assert_called_once()
        workspace_handler._upload.assert_called_once()
        workspace_handler._upload.assert_called_with(archive_name, "some_project_id", cluster_id=None)
        assert response_url == 's3://{}/{}'.format(MOCK_BUCKET_NAME, MOCK_OBJECT_KEY)

    @mock.patch("gradient.utils.PathParser.parse_path",
                return_value=gradient.utils.PathParser.LOCAL_DIR)
    def test_zip_files_and_receive_s3_response_when_workspace_dir_provided(self, _, workspace_handler):
        archive_name = 'foo.zip'

        workspace_handler._zip_workspace = mock.MagicMock()
        workspace_handler._zip_workspace.return_value = archive_name

        response_url = workspace_handler.handle({"projectHandle": "some_project_id", "workspace": "foo/bar"})

        workspace_handler._zip_workspace.assert_called_once()
        workspace_handler._upload.assert_called_once()
        workspace_handler._upload.assert_called_with(archive_name, "some_project_id", cluster_id=None)
        assert response_url == 's3://{}/{}'.format(MOCK_BUCKET_NAME, MOCK_OBJECT_KEY)

    @mock.patch("gradient.utils.PathParser.parse_path",
                return_value=gradient.utils.PathParser.LOCAL_FILE)
    def test_dont_zip_files_and_receive_s3_response_when_workspace_archive_provided(self, _, workspace_handler):
        workspace_handler._zip_workspace = mock.MagicMock()

        response_url = workspace_handler.handle({"projectHandle": "some_project_id", "workspaceArchive": "foo.zip"})

        workspace_handler._zip_workspace.assert_not_called()
        workspace_handler._upload.assert_called_once()
        workspace_handler._upload.assert_called_with(os.path.abspath('foo.zip'), "some_project_id", cluster_id=None)
        assert response_url == 's3://{}/{}'.format(MOCK_BUCKET_NAME, MOCK_OBJECT_KEY)

    @mock.patch("gradient.utils.PathParser.parse_path",
                return_value=gradient.utils.PathParser.LOCAL_FILE)
    def test_dont_zip_files_and_receive_s3_response_when_workspace_archive_provided_with_workspace(self, _,
                                                                                                   workspace_handler):
        workspace_handler._zip_workspace = mock.MagicMock()

        response_url = workspace_handler.handle({'projectHandle': 'foo', 'workspace': 'foo.zip'})

        workspace_handler._zip_workspace.assert_not_called()
        workspace_handler._upload.assert_called_once()
        workspace_handler._upload.assert_called_with(os.path.abspath('foo.zip'), mock_upload_data)
        assert response_url == 's3://{}/{}'.format(MOCK_BUCKET_NAME, MOCK_OBJECT_KEY)

    @mock.patch("gradient.utils.PathParser.parse_path",
                return_value=gradient.utils.PathParser.LOCAL_FILE)
    def test_dont_zip_files_and_receive_s3_response_when_workspace_archive_provided_with_workspace(self, _,
                                                                                                   workspace_handler):
        workspace_handler._zip_workspace = mock.MagicMock()

        response_url = workspace_handler.handle({'projectHandle': 'some_project_id', 'workspace': 'foo.zip'})

        workspace_handler._zip_workspace.assert_not_called()
        workspace_handler._upload.assert_called_once()
        workspace_handler._upload.assert_called_with(os.path.abspath('foo.zip'), "some_project_id", cluster_id=None)
        assert response_url == 's3://{}/{}'.format(MOCK_BUCKET_NAME, MOCK_OBJECT_KEY)
