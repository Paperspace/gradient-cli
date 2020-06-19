import os
import tempfile

from . import s3_uploader, archivers, utils, sdk_exceptions
from .logger import MuteLogger


class WorkspaceHandler(object):
    WORKSPACE_ARCHIVER_CLS = archivers.ZipArchiver

    def __init__(self, logger_=None, archiver_cls=None):
        """

        :param logger_: gradient.logger
        """
        self.logger = logger_ or MuteLogger()
        self.archiver_cls = archiver_cls or self.WORKSPACE_ARCHIVER_CLS

    def _zip_workspace(self, workspace_path, ignore_files):
        zip_file_name = 'workspace.zip'
        zip_file_path = os.path.join(tempfile.gettempdir(), zip_file_name)

        if ignore_files:
            ignore_files = ignore_files.split(",")
            ignore_files = [f.strip() for f in ignore_files]

        zip_archiver = self._get_workspace_archiver()
        zip_archiver.archive(workspace_path, zip_file_path, exclude=ignore_files)

        return zip_file_path

    def handle(self, input_data):
        workspace_path = input_data.get('workspace')
        if workspace_path is None:
            return None

        ignore_files = input_data.get('ignore_files')

        if utils.PathParser.is_remote_path(workspace_path):
            return workspace_path  # nothing to do

        if utils.PathParser.is_local_path(workspace_path):
            return self._handle_local_path(workspace_path, ignore_files)

        raise sdk_exceptions.WrongPathError("Invalid workspace path: {}".format(workspace_path))

    def _handle_local_path(self, workspace_path, ignore_files):
        workspace_path = os.path.abspath(workspace_path)
        if utils.PathParser.parse_path(workspace_path) == utils.PathParser.LOCAL_DIR:
            self.logger.log('Archiving your working directory for upload as your experiment workspace...'
                            '(See https://docs.paperspace.com/gradient/experiments/run-experiments for more '
                            'information.)')
            workspace_path = self._zip_workspace(workspace_path, ignore_files)

        return workspace_path

    def _get_workspace_archiver(self):
        workspace_archiver = self.archiver_cls(logger=self.logger)
        return workspace_archiver


class S3WorkspaceHandler(WorkspaceHandler):
    WORKSPACE_UPLOADER_CLS = s3_uploader.ExperimentFileUploader

    def __init__(self, api_key, client_name=None, uploader_cls=None, *args, **kwargs):
        """
        :param str api_key:
        :param str client_name:
        :param object uploader_cls:
        :param gradient.logger logger_:
        """
        super(S3WorkspaceHandler, self).__init__(*args, **kwargs)
        self.api_key = api_key
        self.client_name = client_name
        self.uploader_cls = uploader_cls or self.WORKSPACE_UPLOADER_CLS

    def handle(self, input_data):
        workspace = super(S3WorkspaceHandler, self).handle(input_data)
        if workspace is None:
            return None

        if utils.PathParser.is_remote_path(workspace):
            return workspace

        project_handle = input_data.get('projectHandle') or input_data.get("project_id")
        cluster_id = input_data.get('clusterId') or input_data.get("cluster_id")
        workspace = self._upload(workspace, project_handle, cluster_id=cluster_id)
        return workspace

    def _upload(self, archive_path, project_id, cluster_id=None):
        uploader = self._get_workspace_uploader(self.api_key)
        workspace = uploader.upload(archive_path, project_id, cluster_id=cluster_id)
        return workspace

    def _get_workspace_uploader(self, api_key):
        workspace_uploader = self.WORKSPACE_UPLOADER_CLS(api_key, logger=self.logger, ps_client_name=self.client_name)
        return workspace_uploader


class S3WorkspaceHandlerWithProgressbar(S3WorkspaceHandler):
    WORKSPACE_ARCHIVER_CLS = archivers.ZipArchiverWithProgressbar

    def _get_workspace_uploader(self, api_key):
        file_uploader = s3_uploader.S3FileUploader(
            s3_uploader.MultipartEncoderWithProgressbar,
            logger=self.logger,
            ps_client_name=self.client_name,
        )
        workspace_uploader = self.uploader_cls(
            api_key,
            uploader=file_uploader,
            logger=self.logger,
            ps_client_name=self.client_name
        )
        return workspace_uploader
