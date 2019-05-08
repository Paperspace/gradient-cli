import os

import click
import mock
import pytest

from paperspace import exceptions
from paperspace.workspace import S3WorkspaceHandler

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
    s3_workspace_handler = S3WorkspaceHandler(mock.MagicMock(), mock.MagicMock())
    s3_workspace_handler._upload = mock.MagicMock()
    s3_workspace_handler._get_upload_data = mock.MagicMock()
    s3_workspace_handler._get_upload_data.return_value = mock_upload_data

    return s3_workspace_handler


class TestWorkspace(object):

    @pytest.mark.parametrize('params', ({'workspace': 'foo', 'workspaceUrl': 'bar'},
                                        {'workspaceUrl': 'ffo', 'workspaceArchive': 'var'},
                                        {'workspaceArchive': 'foo', 'workspace': 'bar'},
                                        {'workspace': 'foo', 'workspaceUrl': 'bar', 'workspaceArchive': 'baz'}))
    def test_raise_exception_when_more_than_one_workspace_provided(self, params, workspace_handler):
        workspace_handler = S3WorkspaceHandler(mock.MagicMock, mock.MagicMock)
        with pytest.raises(click.UsageError):
            workspace_handler.upload_workspace(params)

    def test_dont_upload_if_archive_url_provided(self, workspace_handler):
        workspace_handler.upload_workspace({'workspaceUrl': 'foo'})

        workspace_handler._upload.assert_not_called()

    def test_zip_files_and_receive_s3_response_when_no_dir_provided(self, workspace_handler):
        archive_name = 'foo.zip'

        workspace_handler._zip_workspace = mock.MagicMock()
        workspace_handler._zip_workspace.return_value = archive_name

        response_url = workspace_handler.upload_workspace({'projectHandle': 'foo'})

        workspace_handler._zip_workspace.assert_called_once()
        workspace_handler._upload.assert_called_once()
        workspace_handler._upload.assert_called_with(archive_name, mock_upload_data)
        assert response_url == 's3://{}/{}'.format(MOCK_BUCKET_NAME, MOCK_OBJECT_KEY)

    def test_zip_files_and_receive_s3_response_when_workspace_dir_provided(self, workspace_handler):
        archive_name = 'foo.zip'

        workspace_handler._zip_workspace = mock.MagicMock()
        workspace_handler._zip_workspace.return_value = archive_name

        response_url = workspace_handler.upload_workspace({'projectHandle': 'foo', 'workspace': 'foo/bar'})

        workspace_handler._zip_workspace.assert_called_once()
        workspace_handler._upload.assert_called_once()
        workspace_handler._upload.assert_called_with(archive_name, mock_upload_data)
        assert response_url == 's3://{}/{}'.format(MOCK_BUCKET_NAME, MOCK_OBJECT_KEY)

    def test_dont_zip_files_and_receive_s3_response_when_workspace_archive_provided(self, workspace_handler):
        workspace_handler._zip_workspace = mock.MagicMock()

        response_url = workspace_handler.upload_workspace({'projectHandle': 'foo', 'workspaceArchive': 'foo.zip'})

        workspace_handler._zip_workspace.assert_not_called()
        workspace_handler._upload.assert_called_once()
        workspace_handler._upload.assert_called_with(os.path.abspath('foo.zip'), mock_upload_data)
        assert response_url == 's3://{}/{}'.format(MOCK_BUCKET_NAME, MOCK_OBJECT_KEY)

    @pytest.mark.parametrize('code,exception', ((401, exceptions.ProjectAccessDeniedError),
                                                (403, exceptions.PresignedUrlAccessDeniedError),
                                                (404, exceptions.PresignedUrlUnreachableError)))
    def test_raise_exception_on_40x_presigned_url_response(self, code, exception):
        mock_response = mock.MagicMock()
        mock_response.status_code = code

        workspace_handler = S3WorkspaceHandler(mock.MagicMock(), mock.MagicMock())
        workspace_handler.experiments_api.get.return_value = mock_response

        with pytest.raises(exception):
            workspace_handler._get_upload_data('foo', 'bar')

    def test_return_json_with_presigned_url_response(self):
        mock_response = mock.MagicMock()
        mock_response.json.return_value = mock_upload_response

        workspace_handler = S3WorkspaceHandler(mock.MagicMock(), mock.MagicMock())
        workspace_handler.experiments_api.get.return_value = mock_response

        upload_data = workspace_handler._get_upload_data('foo', 'bar')
        assert upload_data == mock_upload_data

    @mock.patch("paperspace.workspace.requests.post")
    def test_multipart_upload_ok(self, mock_post):
        workspace_handler = S3WorkspaceHandler(mock.MagicMock(), mock.MagicMock())
        workspace_handler._get_files_dict = mock.MagicMock()

        mock_response = mock.MagicMock()
        mock_response.ok = True
        mock_post.return_value = mock_response

        workspace_handler._upload('foo', {'url': 'bar', 'fields': []})

    @mock.patch("paperspace.workspace.requests.post")
    def test_multipart_upload_raises_exception(self, mock_post):
        workspace_handler = S3WorkspaceHandler(mock.MagicMock(), mock.MagicMock())
        workspace_handler._get_files_dict = mock.MagicMock()

        mock_response = mock.MagicMock()
        mock_response.ok = False
        mock_post.return_value = mock_response
        with pytest.raises(exceptions.S3UploadFailedError):
            workspace_handler._upload('foo', {'url': 'bar', 'fields': []})
