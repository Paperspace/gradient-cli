import os

import requests

from .clients.job_client import JobsClient
from .logger import MuteLogger


class S3FilesDownloader(object):
    def download_list(self, sources, destination_dir):
        """

        :param list[Artifact]|tuple[Artifact] sources:
        :param str destination_dir:
        :return:
        """
        for source in sources:
            self.download_file(source, destination_dir)

    def download_file(self, source, destination_dir):
        self._create_directory(destination_dir)

        response = requests.get(source.url)

        self._create_subdirectories(source, destination_dir)
        self._save_file(response, source, destination_dir)

    def _create_directory(self, destination_dir):
        if os.path.exists(destination_dir) and os.path.isdir(destination_dir):
            return

        os.makedirs(destination_dir)

    def _create_subdirectories(self, source, destination_dir):
        file_dirname = os.path.dirname(source.file)
        file_dir_path = os.path.join(destination_dir, file_dirname)
        self._create_directory(file_dir_path)

    def _save_file(self, response, source, destination_dir):
        destination_path = os.path.join(destination_dir, source.file)
        with open(destination_path, "w") as h:
            h.write(response.content)


class JobArtifactsDownloader(object):
    def __init__(self, api_key, logger=MuteLogger()):
        self.api_key = api_key
        self.logger = logger
        self.jobs_client = JobsClient(api_key, logger=logger)

    def download_artifacts(self, job_id, destination):
        files = self._get_files_list(job_id)
        s3_downloader = S3FilesDownloader()
        s3_downloader.download_list(files, destination)

    def _get_files_list(self, job_id):
        files = self.jobs_client.artifacts_list(job_id)
        return files
