import collections
import mimetypes
import os
import tempfile

from . import sdk_exceptions
from .archivers import ZipArchiver
from .clients import http_client
from .config import config
from .logger import MuteLogger
from .utils import MultipartEncoder, MultipartEncoderWithProgressbar


class S3FileUploader(object):
    DEFAULT_MULTIPART_ENCODER_CLS = MultipartEncoder

    def __init__(self, multipart_encoder_cls=None, logger=None, ps_client_name=None):
        """
        :param type(MultipartEncoder) multipart_encoder_cls:
        :param Logger logger:
        """
        self.multipart_encoder_cls = multipart_encoder_cls or self.DEFAULT_MULTIPART_ENCODER_CLS
        self.logger = logger or MuteLogger()
        self.ps_client_name = ps_client_name

    def upload(self, file_path, url, s3_fields=None):
        """Upload a file to S3

        :param str file_path:
        :param str url:
        :param str bucket_name:
        :param dict[str,str] s3_fields:

        """
        # the S3 service requires the file field be the last one in sent object so dict needs to be ordered
        s3_fields = s3_fields or {}
        ordered_s3_fields = collections.OrderedDict(s3_fields)
        with open(file_path, "rb") as file_handle:
            ordered_s3_fields["file"] = (file_path, file_handle)
            multipart_encoder_monitor = self._get_multipart_encoder_monitor(ordered_s3_fields)
            self.logger.debug("Uploading file: {} to url: {}...".format(file_path, url))
            self._upload(url, data=multipart_encoder_monitor)
            self.logger.debug("Uploading completed")

    def _upload(self, url, data):
        """Send data to S3 and raise exception if it was not a success

        :param str url:
        :param encoder.MultipartEncoderMonitor data:
        """
        client = self._get_client(url)
        client.headers = {"Content-Type": data.content_type or ""}
        response = client.post("", data=data)
        if not response.ok:
            raise sdk_exceptions.S3UploadFailedError(response)

    def _get_client(self, url):
        client = http_client.API(url, logger=self.logger, ps_client_name=self.ps_client_name)
        return client

    def _get_multipart_encoder_monitor(self, fields):
        """
        :param dict fields:
        :rtype: encoder.MultipartEncoderMonitor
        """
        multipart_encoder = self.multipart_encoder_cls(fields)
        monitor = multipart_encoder.get_monitor()
        return monitor

    @staticmethod
    def get_bucket_url(bucket_name, s3_fields):
        """
        :param str bucket_name:
        :param dict s3_fields:
        :rtype: str
        """
        s3_object_path = s3_fields["key"]
        url = "s3://{}/{}".format(bucket_name, s3_object_path)
        return url


class S3PutFileUploader(S3FileUploader):
    def _upload(self, url, data):
        """Send data to S3 and raise exception if it was not a success

        :param str url:
        :param encoder.MultipartEncoderMonitor data:
        """
        file_path = data.encoder.fields['file'][0]
        client = self._get_client(url)
        client.headers = {"Content-Type": mimetypes.guess_type(file_path)[0] or ""}

        response = client.put("", data=data)
        if not response.ok:
            raise sdk_exceptions.S3UploadFailedError(response)


class ExperimentFileUploader(object):
    def __init__(self, api_key, uploader=None, logger=None, ps_client_name=None):
        """
        :param str api_key:
        :param S3FileUploader uploader:
        :param Logger logger:
        """
        self.logger = logger or MuteLogger()
        self.experiments_api = http_client.API(
            config.CONFIG_EXPERIMENTS_HOST,
            api_key=api_key,
            logger=self.logger,
            ps_client_name=ps_client_name,
        )
        self.uploader = uploader or S3FileUploader(logger=self.logger, ps_client_name=ps_client_name)

    def upload(self, file_path, project_id, cluster_id=None):
        """Upload file to S3 bucket for a project

        :param str file_path:
        :param str project_id:
        :param str cluster_id:

        :rtype: str
        :return: S3 bucket's URL
        """
        url, bucket_name, fields = self._get_upload_data(file_path, project_id, cluster_id=cluster_id)
        self.uploader.upload(file_path, url, fields)
        bucket_url = self.uploader.get_bucket_url(bucket_name, fields)
        return bucket_url

    def _get_upload_data(self, file_path, project_handle, cluster_id=None):
        """Ask API for data required to upload a file to S3

        :param str file_path:
        :param str project_handle:
        :param str cluster_id:

        :rtype: tuple[str,str,dict]
        :return: URL to which send the file, name of the bucket and a dictionary required by S3 service
        """
        file_name = os.path.basename(file_path)
        params = {"workspaceName": file_name, "projectHandle": project_handle}
        if cluster_id:
            params['clusterHandle'] = cluster_id

        response = self.experiments_api.get("/workspace/get_presigned_url", params=params)
        if response.status_code == 401:
            raise sdk_exceptions.ProjectAccessDeniedError("Access to project denied")
        if response.status_code == 403:
            raise sdk_exceptions.PresignedUrlAccessDeniedError("Access denied")
        if response.status_code == 404:
            raise sdk_exceptions.PresignedUrlUnreachableError("URL not found")
        if not response.ok:
            raise sdk_exceptions.PresignedUrlConnectionError(response.reason)

        try:
            response_data = response.json()
            if response_data["message"] != "success":
                raise sdk_exceptions.PresignedUrlError("Presigned url error: {}".format(response_data))

            url = response_data["data"]["url"]
            bucket_name = response_data["data"]["bucket_name"]
            fields = response_data["data"]["fields"]
        except (KeyError, ValueError):
            raise sdk_exceptions.PresignedUrlMalformedResponseError("Response malformed")

        return url, bucket_name, fields


class S3ProjectFileUploader(ExperimentFileUploader):
    """
    DEPRECATED: This class will be renamed to ExperimentFileUploader in release v0.8
    """
    pass


class S3ModelFileUploader(object):
    DEFAULT_MULTIPART_ENCODER_CLS = MultipartEncoderWithProgressbar

    def __init__(self, api_key, multipart_encoder_cls=None, logger=None, ps_client_name=None, s3uploader=None):
        """
        :param str api_key:
        :param Logger logger:
        """
        self.logger = logger or MuteLogger()
        self.multipart_encoder_cls = multipart_encoder_cls or self.DEFAULT_MULTIPART_ENCODER_CLS
        self.ps_api_client = self._get_client(
            config.CONFIG_HOST,
            api_key=api_key,
            ps_client_name=ps_client_name,
        )
        self.s3uploader = s3uploader or S3PutFileUploader(
            logger=self.logger,
            ps_client_name=ps_client_name,
            multipart_encoder_cls=self.multipart_encoder_cls
        )

    def upload(self, file_path, model_id, cluster_id=None):
        """Upload file to S3 bucket for a project

        :param str file_path:
        :param str model_id:

        :rtype: str
        :return: S3 bucket's URL
        """
        url = self._get_upload_data(file_path, model_id, cluster_id=cluster_id)
        self.s3uploader.upload(file_path, url)
        return url

    def _get_upload_data(self, file_path, model_id, cluster_id=None):
        """Ask API for data required to upload a file to S3

        :param str file_path:
        :param str model_id:

        :rtype: str
        :return: URL to which send the file, name of the bucket and a dictionary required by S3 service
        """
        file_name = os.path.basename(file_path)
        params = {
            "fileName": file_name,
            "modelHandle": model_id,
            "contentType": mimetypes.guess_type(file_path)[0] or "",
        }
        if cluster_id:
            params["clusterId"] = cluster_id

        response = self.ps_api_client.get("/mlModels/getPresignedModelUrl", params=params)
        if not response.ok:
            raise sdk_exceptions.PresignedUrlConnectionError(response.reason)

        try:
            url = response.json()
        except (KeyError, ValueError):
            raise sdk_exceptions.PresignedUrlMalformedResponseError("Response malformed")

        return url

    def _get_client(self, url, ps_client_name=None, api_key=None):
        client = http_client.API(url, logger=self.logger, ps_client_name=ps_client_name, api_key=api_key)
        return client


class S3ModelUploader(S3ModelFileUploader):
    def upload(self, file_path, model_id, cluster_id=None):
        if os.path.isdir(file_path):
            file_path = self._zip_model_directory(file_path)

        return super(S3ModelUploader, self).upload(file_path, model_id, cluster_id=cluster_id)

    def _zip_model_directory(self, dir_path):
        archiver = self._get_archiver()
        archive_path = self._get_archive_path()
        archiver.archive(dir_path, archive_path)
        return archive_path

    def _get_archiver(self):
        return ZipArchiver()

    def _get_archive_path(self):
        archive_file_name = 'model.zip'
        archive_file_path = os.path.join(tempfile.gettempdir(), archive_file_name)
        return archive_file_path


class ExperimentWorkspaceDirectoryUploader(object):
    def __init__(self, api_key, temp_dir=None, archiver=None, project_uploader=None, ps_client_name=None):
        """
        :param str api_key:
        :param str temp_dir:
        :param ZipArchiver archiver:
        :param ExperimentFileUploader project_uploader:
        """
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self.archiver = archiver or ZipArchiver()
        self.ps_client_name = ps_client_name
        self.project_uploader = project_uploader or ExperimentFileUploader(api_key, ps_client_name=ps_client_name)

    def upload(self, workspace_dir_path, project_id, exclude=None, temp_file_name="temp.zip"):
        """Archive and upload a workspace directory

        :param str workspace_dir_path:
        :param str project_id:
        :param list|tuple|None exclude:
        :param str temp_file_name:

        :rtype: str
        :return: URL to the S3 bucket
        """
        archive_path = self.get_archive_path(temp_file_name)
        self.archiver.archive(workspace_dir_path, archive_path, exclude=exclude)
        bucket_url = self.project_uploader.upload(archive_path, project_id)
        return bucket_url

    def get_archive_path(self, temp_file_name):
        archive_path = os.path.join(self.temp_dir, temp_file_name)
        return archive_path


class S3WorkspaceDirectoryUploader(ExperimentWorkspaceDirectoryUploader):
    """
    DEPRECATED: This class will be renamed to ExperimentWorkspaceDirectoryUploader in release v0.8
    """
    pass


class DeploymentWorkspaceDirectoryUploader(object):
    def __init__(self, api_key, uploader=None, logger=None, ps_client_name=None):
        """
        :param str api_key:
        :param S3PutFileUploader uploader:
        :param Logger logger:
        """
        self.logger = logger or MuteLogger()
        self.ps_api_client = http_client.API(
            config.CONFIG_HOST,
            api_key=api_key,
            logger=self.logger,
            ps_client_name=ps_client_name,
        )
        self.uploader = S3PutFileUploader(logger=self.logger, ps_client_name=ps_client_name)

    def _get_upload_data(self, file_path, project_id, cluster_id=None):
        """Ask API for data required to upload deployment workspace a file to S3

        :param str file_path:
        :param str project_id:
        :param str cluster_id:

        :rtype: str
        :return: URL to which send the file, name of the bucket and a dictionary required by S3 service
        """
        file_name = os.path.basename(file_path)
        params = {
            "fileName": file_name,
            "contentType": mimetypes.guess_type(file_path)[0] or "",
        }
        if project_id:
            params['projectId'] = project_id
        if cluster_id:
            params['clusterHandle'] = cluster_id
        response = self.ps_api_client.get("/deployments/getPresignedDeploymentUrl", params=params)
        if not response.ok:
            raise sdk_exceptions.PresignedUrlConnectionError(response.reason)

        try:
            response_data = response.json()
            presigned_url = response_data['presignedUrl']
            bucket_name = response_data['bucketName']
            workspace_url = response_data['workspaceUrl']
        except (KeyError, ValueError):
            raise sdk_exceptions.PresignedUrlMalformedResponseError("Response malformed")

        return presigned_url, bucket_name, workspace_url

    def upload(self, file_path, project_id=None, cluster_id=None, **kwargs):
        """Upload file to S3 bucket for a project

        :param str file_path:
        :param str project_id:
        :param str cluster_id:

        :rtype: str
        :return: S3 bucket's URL
        """
        url, bucket_name, workspace_url = self._get_upload_data(file_path, project_id, cluster_id)
        self.uploader.upload(file_path, url)
        return workspace_url
