import sys

import mock
from pytest import fixture

from gradient.api_sdk.s3_uploader import S3FileUploader, S3ProjectFileUploader, S3ModelFileUploader, \
    S3WorkspaceDirectoryUploader

open_path = "builtins.open"
if sys.version_info[0] < 3:
    open_path = "__builtin__.open"


@fixture
def client():
    client = mock.MagicMock()
    client.get = mock.MagicMock()
    client.put = mock.MagicMock()
    client.post = mock.MagicMock()
    return client


@fixture
def file_uploader(client):
    mock_get_client = mock.MagicMock()
    mock_get_client.return_value = client

    mock_encoder_class = mock.Mock(spec=S3FileUploader.DEFAULT_MULTIPART_ENCODER_CLS)
    uploader = S3FileUploader(multipart_encoder_cls=mock_encoder_class)
    uploader._get_client = mock_get_client
    return uploader


def get_ps_exp_valid_response(mock_url):
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.ok = True
    mock_response.json.return_value = {
        "message": "success",
        "data": {
            "url": mock_url,
            "bucket_name": "bucketname",
            "fields": {
                "key": "foo_key"
            }
        }
    }
    return mock_response


class TestS3FileUploader(object):
    def test_should_post_file_data_and_return_valid_url(self, client, file_uploader):
        upload_url = "s3://url"
        _mock_open = mock.mock_open(read_data="data")
        with mock.patch(open_path, _mock_open) as mock_file:
            file_uploader.upload("filename", upload_url, {"key": "foo"})

        file_uploader._get_client.assert_called_with(upload_url)
        client.post.assert_called()


class TestS3ProjectFileUploader(object):
    def test_should_post_file_data_and_return_valid_url(self, client, file_uploader):
        upload_url = "s3://url"
        mock_response = get_ps_exp_valid_response(upload_url)

        mock_api_client = mock.MagicMock()
        mock_api_client.get.return_value = mock_response

        uploader = S3ProjectFileUploader("api_key", s3uploader=file_uploader)
        uploader.experiments_api = mock_api_client

        _mock_open = mock.mock_open(read_data="data")
        with mock.patch(open_path, _mock_open) as mock_file:
            uploader.upload("foo", "pjHandle", "clHandle")

        file_uploader._get_client.assert_called_with(upload_url)
        client.post.assert_called()


class TestS3ModelFileUploader(object):
    def test_should_post_file_data_and_return_valid_url(self, client, file_uploader):
        upload_url = "s3://url"

        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = upload_url

        mock_api_client = mock.MagicMock()
        mock_api_client.get.return_value = mock_response

        uploader = S3ModelFileUploader("api_key", s3uploader=file_uploader)
        uploader.ps_api_client = mock_api_client
        _mock_open = mock.mock_open(read_data="data")

        with mock.patch(open_path, _mock_open) as mock_file:
            uploader.upload("foo", "mdHandle")

        file_uploader._get_client.assert_called_with(upload_url)
        client.post.assert_called()


class TestS3WorkspaceDirectoryUploader(object):

    def test_should_post_file_data_and_return_valid_url(self, client, file_uploader):
        upload_url = "s3://url"

        mock_response = get_ps_exp_valid_response(upload_url)

        mock_api_client = mock.MagicMock()
        mock_api_client.get.return_value = mock_response
        project_uploader = S3ProjectFileUploader("api_key", s3uploader=file_uploader)
        project_uploader.experiments_api = mock_api_client

        uploader = S3WorkspaceDirectoryUploader(api_key="api_key", archiver=mock.MagicMock(),
                                                project_uploader=project_uploader)

        _mock_open = mock.mock_open(read_data="data")
        with mock.patch(open_path, _mock_open) as mock_file:
            uploader.upload("foo", "mdHandle")

        file_uploader._get_client.assert_called_with(upload_url)
        client.post.assert_called()
