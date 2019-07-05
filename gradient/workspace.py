import os
import zipfile
from collections import OrderedDict

import click
import progressbar
import requests
from requests_toolbelt.multipart import encoder

from gradient import logger, utils
from gradient.exceptions import S3UploadFailedError, PresignedUrlUnreachableError, \
    PresignedUrlAccessDeniedError, PresignedUrlConnectionError, ProjectAccessDeniedError, \
    PresignedUrlMalformedResponseError, PresignedUrlError


class MultipartEncoder(object):
    def __init__(self, fields):
        mp_encoder = encoder.MultipartEncoder(fields=fields)
        self.monitor = encoder.MultipartEncoderMonitor(mp_encoder, callback=self._create_callback(mp_encoder))

    def get_monitor(self):
        return self.monitor

    @staticmethod
    def _create_callback(encoder_obj):
        bar = progressbar.ProgressBar(max_value=encoder_obj.len)

        def callback(monitor):
            if monitor.bytes_read == bar.max_value:
                bar.finish()
            else:
                bar.update(monitor.bytes_read)

        return callback


class WorkspaceHandler(object):
    def __init__(self, logger_=None):
        """

        :param logger_: gradient.logger
        """
        self.logger = logger_ or logger.Logger()
        self.archive_path = None
        self.archive_basename = None

    @staticmethod
    def _retrieve_file_paths(dir_name, ignored_files=None):
        # setup file paths variable
        file_paths = {}

        exclude = ['.git', '.idea', '.pytest_cache']
        if ignored_files:
            exclude += ignored_files.split(',')

        # Read all directory, subdirectories and file lists
        for root, dirs, files in os.walk(dir_name, topdown=True):
            dirs[:] = [d for d in dirs if d not in exclude]
            for filename in files:
                # Create the full filepath by using os module.
                relpath = os.path.relpath(root, dir_name)
                if relpath == '.':
                    file_path = filename
                else:
                    file_path = os.path.join(os.path.relpath(root, dir_name), filename)
                if file_path not in exclude:
                    file_paths[file_path] = os.path.join(root, filename)

        return file_paths

    def _zip_workspace(self, workspace_path, ignore_files):
        if not workspace_path:
            workspace_path = '.'
            zip_file_name = os.path.basename(os.getcwd()) + '.zip'
        else:
            zip_file_name = os.path.basename(workspace_path) + '.zip'

        zip_file_path = os.path.join(workspace_path, zip_file_name)

        if os.path.exists(zip_file_path):
            self.logger.log('Removing existing archive')
            os.remove(zip_file_path)
        file_paths = self._retrieve_file_paths(workspace_path, ignore_files)

        self.logger.log('Creating zip archive: %s' % zip_file_name)
        zip_file = zipfile.ZipFile(zip_file_path, 'w')

        bar = progressbar.ProgressBar(max_value=len(file_paths))

        with zip_file:
            i = 0
            for relpath, abspath in file_paths.items():
                i += 1
                self.logger.debug('Adding %s to archive' % relpath)
                zip_file.write(abspath, arcname=relpath)
                bar.update(i)
        bar.finish()
        self.logger.log('\nFinished creating archive: %s' % zip_file_name)
        return zip_file_path

    def handle(self, input_data):
        workspace_archive, workspace_path, workspace_url = self._validate_input(input_data)
        ignore_files = input_data.get('ignore_files')

        if workspace_url:
            return workspace_url  # nothing to do

        # Should be removed as soon it won't be necessary by PS_API
        if workspace_path == 'none':
            return 'none'
        if workspace_archive:
            archive_path = os.path.abspath(workspace_archive)
        else:
            self.logger.log('Archiving your working directory for upload as your experiment workspace...'
                            '(See https://docs.paperspace.com/gradient/experiments/run-experiments for more information.)')
            archive_path = self._zip_workspace(workspace_path, ignore_files)
        self.archive_path = archive_path
        self.archive_basename = os.path.basename(archive_path)
        return archive_path

    @staticmethod
    def _validate_input(input_data):
        utils.validate_workspace_input(input_data)

        workspace_url = input_data.get('workspaceUrl')
        workspace_path = input_data.get('workspace')
        workspace_archive = input_data.get('workspaceArchive')

        if workspace_path not in ("none", None):
            path_type = utils.PathParser().parse_path(workspace_path)

            if path_type == utils.PathParser.LOCAL_DIR:
                input_data["workspace"] = workspace_path
            else:
                if path_type == utils.PathParser.LOCAL_FILE:
                    input_data["workspaceArchive"] = workspace_archive = workspace_path
                elif path_type in (utils.PathParser.GIT_URL, utils.PathParser.S3_URL):
                    input_data["workspaceUrl"] = workspace_url = workspace_path

                workspace_path = None
                input_data.pop("workspace", None)

        return workspace_archive, workspace_path, workspace_url


class S3WorkspaceHandler(WorkspaceHandler):
    def __init__(self, experiments_api, logger_=None):
        """

        :param experiments_api: gradient.client.API
        :param logger_: gradient.logger
        """
        super(S3WorkspaceHandler, self).__init__(logger_=logger_)
        self.experiments_api = experiments_api

    def handle(self, input_data):
        workspace = super(S3WorkspaceHandler, self).handle(input_data)
        if not self.archive_path:
            return workspace
        archive_path = workspace
        file_name = os.path.basename(archive_path)
        project_handle = input_data['projectHandle']

        s3_upload_data = self._get_upload_data(file_name, project_handle)

        bucket_name = s3_upload_data['bucket_name']
        s3_object_path = s3_upload_data['fields']['key']

        self.logger.log('Uploading zipped workspace to S3')

        self._upload(archive_path, s3_upload_data)

        self.logger.log('\nUploading completed')

        return 's3://{}/{}'.format(bucket_name, s3_object_path)

    def _upload(self, archive_path, s3_upload_data):
        files = self._get_files_dict(archive_path)
        fields = OrderedDict(s3_upload_data['fields'])
        fields.update(files)

        monitor = MultipartEncoder(fields).get_monitor()
        s3_response = requests.post(s3_upload_data['url'], data=monitor, headers={'Content-Type': monitor.content_type})
        self.logger.debug("S3 upload response: {}".format(s3_response.headers))
        if not s3_response.ok:
            raise S3UploadFailedError(s3_response)

    def _get_files_dict(self, archive_path):
        files = {'file': (archive_path, open(archive_path, 'rb'))}
        return files

    def _get_upload_data(self, file_name, project_handle):
        response = self.experiments_api.get("/workspace/get_presigned_url",
                                            params={'workspaceName': file_name, 'projectHandle': project_handle})
        if response.status_code == 401:
            raise ProjectAccessDeniedError(project_handle)
        if response.status_code == 403:
            raise PresignedUrlAccessDeniedError
        if response.status_code == 404:
            raise PresignedUrlUnreachableError
        if not response.ok:
            raise PresignedUrlConnectionError(response.reason)

        response_content = response.json()
        try:
            response_message = response_content['message']
            response_data = response_content['data']
        except KeyError:
            raise PresignedUrlMalformedResponseError(response_content)
        if response_message != 'success':
            raise PresignedUrlError(response)
        return response_data
