import collections
import os
import tempfile
import zipfile

import progressbar
from requests_toolbelt.multipart import encoder

from gradient.api_sdk import exceptions
from gradient.api_sdk.clients import http_client
from gradient.api_sdk.logger import MuteLogger
from gradient.config import config


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
    DEFAULT_EXCLUDED_PATHS = [".git", ".idea", ".pytest_cache"]

    def __init__(self, logger=MuteLogger()):
        self.logger = logger
        self.default_excluded_paths = self.DEFAULT_EXCLUDED_PATHS

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
            if relative_path in excluded_paths:
                continue

            for filename in files:
                # Create the full filepath by using os module.
                if relative_path == '.':
                    file_path = filename
                else:
                    file_path = os.path.join(os.path.relpath(root, input_path), filename)

                if file_path not in excluded_paths:
                    file_paths[file_path] = os.path.join(root, filename)

        return file_paths

    def _archive(self, file_paths, output_file_path):
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
        self.bar = progressbar.ProgressBar(max_value=len(file_paths))
        super(ZipArchiverWithProgressbar, self)._archive(file_paths, output_file_path)
        self.bar.finish()

    def _archive_iterate_callback(self, i):
        self.bar.update(i)


class S3FileUploader(object):
    DEFAULT_MULTIPART_ENCODER_CLS = MultipartEncoder

    def __init__(self, multipart_encoder_cls=None, logger=MuteLogger()):
        self.multipart_encoder_cls = multipart_encoder_cls or self.DEFAULT_MULTIPART_ENCODER_CLS
        self.logger = logger

    def upload(self, file_path, url, bucket_name, s3_fields):
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
        client = self._get_client(url)
        response = client.post("", data=data)
        if not response.ok:
            raise exceptions.S3UploadFailedError(response)

    def _get_client(self, url):
        client = http_client.API(url, logger=self.logger)
        return client

    def _get_multipart_encoder_monitor(self, fields):
        multipart_encoder = self.multipart_encoder_cls(fields)
        monitor = multipart_encoder.get_monitor()
        return monitor

    def _get_bucket_url(self, bucket_name, s3_fields):
        s3_object_path = s3_fields["key"]
        url = "s3://{}/{}".format(bucket_name, s3_object_path)
        return url


class S3ProjectFileUploader(object):
    def __init__(self, api_key, s3uploader=None, logger=MuteLogger()):
        self.s3uploader = s3uploader or S3FileUploader()
        self.experiments_api = http_client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)
        self.logger = logger

    def upload(self, file_path, project_id):
        url, bucket_name, s3_fields = self._get_upload_data(file_path, project_id)
        bucket_url = self.s3uploader.upload(file_path, url, bucket_name, s3_fields)
        return bucket_url

    def _get_upload_data(self, file_path, project_handle):
        file_name = os.path.basename(file_path)
        response = self.experiments_api.get("/workspace/get_presigned_url",
                                            params={'workspaceName': file_name, 'projectHandle': project_handle})
        if response.status_code == 401:
            raise exceptions.ProjectAccessDeniedError("Access to project denied")
        if response.status_code == 403:
            raise exceptions.PresignedUrlAccessDeniedError("Access denied")
        if response.status_code == 404:
            raise exceptions.PresignedUrlUnreachableError("URL not found")
        if not response.ok:
            raise exceptions.PresignedUrlConnectionError(response.reason)

        try:
            response_data = response.json()
            if response_data["message"] != "success":
                raise exceptions.PresignedUrlError("Presigned url error: {}".format(response_data))

            url = response_data["data"]["url"]
            bucket_name = response_data["data"]["bucket_name"]
            s3_fields = response_data["data"]["fields"]
        except (KeyError, ValueError):
            raise exceptions.PresignedUrlMalformedResponseError("Response malformed")

        return url, bucket_name, s3_fields


class S3WorkspaceDirectoryUploader(object):
    def __init__(self, api_key, temp_dir=None, archiver=None, project_uploader=None):
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self.archiver = archiver or ZipArchiver()
        self.project_uploader = project_uploader or S3ProjectFileUploader(api_key)
        self.experiments_api = http_client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=api_key)

    def upload(self, workspace_dir_path, project_id, exclude=None, temp_file_name="temp.zip"):
        archive_path = self.get_archive_path(temp_file_name)
        self.archiver.archive(workspace_dir_path, archive_path, exclude=exclude)
        bucket_url = self.project_uploader.upload(archive_path, project_id)
        return bucket_url

    def get_archive_path(self, temp_file_name):
        archive_path = os.path.join(self.temp_dir, temp_file_name)
        return archive_path
