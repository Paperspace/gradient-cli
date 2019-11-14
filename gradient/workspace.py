import os
import tempfile

import progressbar
from requests_toolbelt.multipart import encoder

from gradient import utils
from gradient.api_sdk import s3_uploader
from gradient.logger import Logger


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


class WorkspaceHandler(object):
    WORKSPACE_ARCHIVER_CLS = s3_uploader.ZipArchiver

    def __init__(self, logger_=None):
        """

        :param logger_: gradient.logger
        """
        self.logger = logger_ or Logger()
        self.archive_path = None
        self.archive_basename = None

    def _zip_workspace(self, workspace_path, ignore_files):
        if not workspace_path:
            workspace_path = '.'
            zip_file_name = os.path.basename(os.getcwd()) + '.zip'
        else:
            zip_file_name = os.path.basename(workspace_path) + '.zip'

        zip_file_path = os.path.join(tempfile.gettempdir(), zip_file_name)

        if ignore_files:
            ignore_files = ignore_files.split(",")
        zip_archiver = self._get_workspace_archiver()
        zip_archiver.archive(workspace_path, zip_file_path, exclude=ignore_files)

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

    def _get_workspace_archiver(self):
        workspace_archiver = self.WORKSPACE_ARCHIVER_CLS(logger=self.logger)
        return workspace_archiver

    @staticmethod
    def _validate_input(input_data):
        utils.validate_workspace_input(input_data)

        workspace_url = input_data.get('workspaceUrl') or input_data.get("workspace_url")
        workspace_path = input_data.get('workspace')
        workspace_archive = input_data.get('workspaceArchive') or input_data.get("workspace_archive")

        if workspace_path not in ("none", None):
            path_type = utils.PathParser.parse_path(workspace_path)

            if path_type != utils.PathParser.LOCAL_DIR:
                if path_type == utils.PathParser.LOCAL_FILE:
                    workspace_archive = workspace_path
                elif path_type in (utils.PathParser.GIT_URL, utils.PathParser.S3_URL):
                    workspace_url = workspace_path

                workspace_path = None

        return workspace_archive, workspace_path, workspace_url


class S3WorkspaceHandler(WorkspaceHandler):
    WORKSPACE_UPLOADER_CLS = s3_uploader.S3ProjectFileUploader

    def __init__(self, api_key, logger_=None):
        """
        :param str api_key:
        :param gradient.logger.Logger logger_:
        """
        super(S3WorkspaceHandler, self).__init__(logger_=logger_)
        self.api_key = api_key

    def handle(self, input_data):
        workspace = super(S3WorkspaceHandler, self).handle(input_data)
        if not self.archive_path:
            return workspace

        archive_path = workspace
        project_handle = input_data.get('projectHandle') or input_data["project_id"]
        workspace = self._upload(archive_path, project_handle)
        return workspace

    def _upload(self, archive_path, project_id):
        uploader = self._get_workspace_uploader(self.api_key)
        workspace = uploader.upload(archive_path, project_id)
        return workspace

    def _get_workspace_uploader(self, api_key):
        workspace_uploader = self.WORKSPACE_UPLOADER_CLS(api_key, logger=self.logger)
        return workspace_uploader


class S3WorkspaceHandlerWithProgressbar(S3WorkspaceHandler):
    WORKSPACE_ARCHIVER = s3_uploader.ZipArchiverWithProgressbar

    def _get_workspace_uploader(self, api_key):
        file_uploader = s3_uploader.S3FileUploader(s3_uploader.MultipartEncoderWithProgressbar, logger=self.logger)
        workspace_uploader = self.WORKSPACE_UPLOADER_CLS(api_key, s3uploader=file_uploader, logger=self.logger)
        return workspace_uploader
