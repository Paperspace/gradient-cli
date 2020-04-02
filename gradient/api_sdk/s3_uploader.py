import collections
import fnmatch
import mimetypes
import os
import tempfile
import zipfile

import progressbar
from requests_toolbelt.multipart import encoder

from . import sdk_exceptions
from .clients import http_client
from .config import config
from .logger import MuteLogger


class MultipartEncoder(object):
    def __init__(self, fields):
        mp_encoder = encoder.MultipartEncoder(fields=fields)
        self.monitor = encoder.MultipartEncoderMonitor(mp_encoder, callback=self._create_callback(mp_encoder))

    def get_monitor(self):
        return self.monitor

    @staticmethod
    def _create_callback(encoder_obj):
        pass


class MultipartEncoderWithProgressbar(MultipartEncoder):
    @staticmethod
    def _create_callback(encoder_obj):
        bar = progressbar.ProgressBar(max_value=encoder_obj.len)

        def callback(monitor):
            if monitor.bytes_read == bar.max_value:
                bar.finish()
            else:
                bar.update(monitor.bytes_read)

        return callback


class ZipArchiver(object):
    DEFAULT_EXCLUDED_PATHS = [
        os.path.join(".git", "*"),
        os.path.join(".idea", "*"),
        os.path.join(".pytest_cache", "*"),
    ]

    def __init__(self, logger=None):
        self.logger = logger or MuteLogger()
        self.default_excluded_paths = self.DEFAULT_EXCLUDED_PATHS[:]

    def archive(self, input_dir_path, output_file_path, overwrite_existing_archive=True, exclude=None):
        """

        :param str input_dir_path:
        :param str output_file_path:
        :param bool overwrite_existing_archive:
        :param list|tuple|None exclude:
        """
        excluded_paths = self.get_excluded_paths(exclude)

        file_paths = self.get_file_paths(input_dir_path, excluded_paths)

        if os.path.exists(output_file_path):
            if not overwrite_existing_archive:
                raise IOError("File already exists")

            self.logger.log('Removing existing archive')
            os.remove(output_file_path)

        self.logger.log('Creating zip archive: %s' % output_file_path)
        self._archive(file_paths, output_file_path)
        self.logger.log('Finished creating archive: %s' % output_file_path)

    def get_excluded_paths(self, exclude=None):
        """
        :param list|tuple|None exclude:
        :rtype: set
        """
        if exclude is None:
            exclude = []

        excluded_paths = set(self.default_excluded_paths)
        excluded_paths.update(exclude)
        return excluded_paths

    @staticmethod
    def get_file_paths(input_path, excluded_paths=None):
        """Get a dictionary of all files in input_dir excluding specified in excluded_paths

        :param str input_path:
        :param list|tuple|set|None excluded_paths:
        :return: dictionary with full paths as values as keys and relative paths
        :rtype: dict[str,str]
        """
        if excluded_paths is None:
            excluded_paths = []

        file_paths = {}

        # Read all directory, subdirectories and file lists
        for root, dirs, files in os.walk(input_path):
            relative_path = os.path.relpath(root, input_path)

            for filename in files:
                # Create the full filepath by using os module.
                if relative_path == '.':
                    file_path = filename
                else:
                    file_path = os.path.join(os.path.relpath(root, input_path), filename)

                if any(fnmatch.fnmatch(file_path, pattern) for pattern in excluded_paths):
                    continue

                if file_path not in excluded_paths:
                    file_paths[file_path] = os.path.join(root, filename)

        return file_paths

    def _archive(self, file_paths, output_file_path):
        """Create ZIP archive and add files to it

        :param dict[str,str] file_paths:
        :param str output_file_path:
        """
        zip_file = zipfile.ZipFile(output_file_path, 'w')
        with zip_file:
            i = 0
            for relative_path, abspath in file_paths.items():
                i += 1
                self.logger.debug('Adding %s to archive' % relative_path)
                zip_file.write(abspath, arcname=relative_path)
                self._archive_iterate_callback(i)

    def _archive_iterate_callback(self, i):
        pass


class ZipArchiverWithProgressbar(ZipArchiver):
    def _archive(self, file_paths, output_file_path):
        """Create ZIP archive and add files to it and show progress bar in terminal

        :param dict[str,str] file_paths:
        :param str output_file_path:
        """
        self.bar = progressbar.ProgressBar(max_value=len(file_paths))
        super(ZipArchiverWithProgressbar, self)._archive(file_paths, output_file_path)
        self.bar.finish()

    def _archive_iterate_callback(self, i):
        self.bar.update(i)


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

    def upload(self, file_path, url, bucket_name, s3_fields):
        """Upload a file to S3

        :param str file_path:
        :param str url:
        :param str bucket_name:
        :param dict[str,str] s3_fields:

        :rtype: str
        :return: URL to S3 bucket
        """
        # the S3 service requires the file field be the last one in sent object so dict needs to be ordered
        ordered_s3_fields = collections.OrderedDict(s3_fields)
        with open(file_path, "rb") as file_handle:
            ordered_s3_fields["file"] = (file_path, file_handle)
            multipart_encoder_monitor = self._get_multipart_encoder_monitor(ordered_s3_fields)
            self.logger.debug("Uploading file: {} to bucket: {}...".format(file_path, bucket_name))
            self._upload(url, data=multipart_encoder_monitor)
            self.logger.debug("Uploading completed")

        bucket_url = self._get_bucket_url(bucket_name, s3_fields)
        return bucket_url

    def _upload(self, url, data):
        """Send data to S3 and raise exception if it was not a success

        :param str url:
        :param encoder.MultipartEncoderMonitor data:
        """
        client = self._get_client(url)
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
    def _get_bucket_url(bucket_name, s3_fields):
        """
        :param str bucket_name:
        :param dict s3_fields:
        :rtype: str
        """
        s3_object_path = s3_fields["key"]
        url = "s3://{}/{}".format(bucket_name, s3_object_path)
        return url


class S3ProjectFileUploader(object):
    def __init__(self, api_key, s3uploader=None, logger=None, ps_client_name=None):
        """
        :param str api_key:
        :param S3FileUploader s3uploader:
        :param Logger logger:
        """
        self.logger = logger or MuteLogger()
        self.experiments_api = http_client.API(
            config.CONFIG_EXPERIMENTS_HOST,
            api_key=api_key,
            logger=self.logger,
            ps_client_name=ps_client_name,
        )
        self.s3uploader = s3uploader or S3FileUploader(logger=self.logger, ps_client_name=ps_client_name)

    def upload(self, file_path, project_id, cluster_id=None):
        """Upload file to S3 bucket for a project

        :param str file_path:
        :param str project_id:
        :param str cluster_id:

        :rtype: str
        :return: S3 bucket's URL
        """
        url, bucket_name, s3_fields = self._get_upload_data(file_path, project_id, cluster_id=cluster_id)
        bucket_url = self.s3uploader.upload(file_path, url, bucket_name, s3_fields)
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
            s3_fields = response_data["data"]["fields"]
        except (KeyError, ValueError):
            raise sdk_exceptions.PresignedUrlMalformedResponseError("Response malformed")

        return url, bucket_name, s3_fields


class S3ModelFileUploader(object):
    DEFAULT_MULTIPART_ENCODER_CLS = MultipartEncoderWithProgressbar

    def __init__(self, api_key, multipart_encoder_cls=None, logger=None, ps_client_name=None):
        """
        :param str api_key:
        :param Logger logger:
        """
        self.logger = logger or MuteLogger()
        self.multipart_encoder_cls = multipart_encoder_cls or self.DEFAULT_MULTIPART_ENCODER_CLS
        self.client = self._get_client(
            config.CONFIG_HOST,
            api_key=api_key,
            ps_client_name=ps_client_name,
        )

    def upload(self, file_path, model_id):
        """Upload file to S3 bucket for a project

        :param str file_path:
        :param str model_id:

        :rtype: str
        :return: S3 bucket's URL
        """
        url = self._get_upload_data(file_path, model_id)
        bucket_url = self._upload(file_path, url)
        return bucket_url

    def _get_upload_data(self, file_path, model_id):
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

        response = self.client.get("/mlModels/getPresignedModelUrl", params=params)
        if not response.ok:
            raise sdk_exceptions.PresignedUrlConnectionError(response.reason)

        try:
            url = response.json()
        except (KeyError, ValueError):
            raise sdk_exceptions.PresignedUrlMalformedResponseError("Response malformed")

        return url

    def _upload(self, file_path, url):
        """Upload a file to S3

        :param str file_path:
        :param str url:

        :rtype: str
        :return: URL to S3 bucket
        """
        # the S3 service requires the file field be the last one in sent object so dict needs to be ordered
        ordered_s3_fields = collections.OrderedDict()

        client = self._get_client(url)
        client.headers = {"Content-Type": mimetypes.guess_type(file_path)[0] or ""}
        with open(file_path, "rb") as file_handle:
            ordered_s3_fields["file"] = (file_path, file_handle)
            multipart_encoder_monitor = self._get_multipart_encoder_monitor(ordered_s3_fields)
            response = self._send_upload_request(client, data=multipart_encoder_monitor)
            if not response.ok:
                raise sdk_exceptions.S3UploadFailedError(response)
            self.logger.debug("Uploading completed")

        return url

    def _get_multipart_encoder_monitor(self, fields):
        """
        :param dict fields:
        :rtype: encoder.MultipartEncoderMonitor
        """
        multipart_encoder = self.multipart_encoder_cls(fields)
        monitor = multipart_encoder.get_monitor()
        return monitor

    def _send_upload_request(self, client, data):
        response = client.put("", data=data)
        return response

    def _get_client(self, url, ps_client_name=None, api_key=None):
        client = http_client.API(url, logger=self.logger, ps_client_name=ps_client_name, api_key=api_key)
        return client


class S3WorkspaceDirectoryUploader(object):
    def __init__(self, api_key, temp_dir=None, archiver=None, project_uploader=None, ps_client_name=None):
        """
        :param str api_key:
        :param str temp_dir:
        :param ZipArchiver archiver:
        :param S3ProjectFileUploader project_uploader:
        """
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self.archiver = archiver or ZipArchiver()
        self.ps_client_name = ps_client_name
        self.project_uploader = project_uploader or S3ProjectFileUploader(api_key, ps_client_name=ps_client_name)

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
