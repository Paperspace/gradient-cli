import os
import tempfile

from . import s3_uploader, archivers, utils
from .logger import MuteLogger


class WorkspaceHandler(object):
    WORKSPACE_ARCHIVER_CLS = archivers.ZipArchiver

    def __init__(self, logger_=None, archiver_cls=None):
        """

        :param logger_: gradient.logger
        """
        self.logger = logger_ or MuteLogger()
        self.archive_path = None
        self.archive_basename = None
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
        workspace_archiver = self.archiver_cls(logger=self.logger)
        return workspace_archiver

    @staticmethod
    def _validate_input(input_data):
        workspace_path = input_data.get('workspace')
        workspace_archive = None
        workspace_url = None

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
        if not self.archive_path:
            return workspace

        archive_path = workspace
        project_handle = input_data.get('projectHandle') or input_data.get("project_id")
        cluster_id = input_data.get('clusterId') or input_data.get("cluster_id")
        workspace = self._upload(archive_path, project_handle, cluster_id=cluster_id)
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
