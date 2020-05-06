import abc
import os
import time

import requests
import six

from . import sdk_exceptions
from .clients import JobsClient, ModelsClient
from .clients.base_client import BaseClient
from .logger import MuteLogger


class S3FilesDownloader(object):
    def __init__(self, logger=MuteLogger()):
        self.logger = logger
        self.file_download_retries = 8

    def download_list(self, sources, destination_dir):
        """

        :param tuple[tuple[str,str]] sources: tuple/list of (file_path, file_url) pairs
        :param str destination_dir:
        """
        for source in sources:
            self.download_file(source, destination_dir, max_retries=self.file_download_retries)

    def download_file(self, source, destination_dir, max_retries=0):
        self._create_directory(destination_dir)

        file_path, file_url = source
        self.logger.log("Downloading: {}".format(file_path))

        # Trying to download several times in case of connection error with S3.
        # The error seems to occur randomly but adding short sleep between retries helps a bit
        for _ in range(max_retries + 1):
            try:
                response = requests.get(file_url)
                break
            except requests.exceptions.ConnectionError:
                self.logger.debug("Downloading {} resulted in error. Trying again...".format(file_path))
                time.sleep(0.1)
        else:  # break statement not executed - ConnectionError `max_retries` times
            raise sdk_exceptions.ResourceFetchingError("Downloading {} resulted in error".format(file_path))

        self._create_subdirectories(file_path, destination_dir)
        self._save_file(response, file_path, destination_dir)

    def _create_directory(self, destination_dir):
        if os.path.exists(destination_dir) and os.path.isdir(destination_dir):
            return

        os.makedirs(destination_dir)

    def _create_subdirectories(self, file_path, destination_dir):
        file_dirname = os.path.dirname(file_path)
        file_dir_path = os.path.join(destination_dir, file_dirname)
        self._create_directory(file_dir_path)

    def _save_file(self, response, file_path, destination_dir):
        destination_path = os.path.join(destination_dir, file_path)
        try:
            with open(destination_path, "wb") as h:
                h.write(response.content)
        except TypeError:  # in py3 TypeError is raised when trying to write str in bytes mode so trying in txt mode
            with open(destination_path, "w") as h:
                h.write(response.content)


@six.add_metaclass(abc.ABCMeta)
class ResourceDownloader(object):
    CLIENT_CLASS = None

    def __init__(self, api_key, logger=MuteLogger(), ps_client_name=None):
        self.api_key = api_key
        self.logger = logger
        self.ps_client_name = ps_client_name
        self.client = self._build_client(self.CLIENT_CLASS, api_key, logger=logger)

    def download(self, job_id, destination):
        files = self._get_files_list(job_id)
        s3_downloader = S3FilesDownloader(logger=self.logger)
        s3_downloader.download_list(files, destination)

    @abc.abstractmethod
    def _get_files_list(self, job_id):
        """
        :param str job_id:
        :returns: Tuple of (file path, url) pairs
        :rtype: tuple[tuple[str,str]]
        """
        pass

    def _build_client(self, client_class, *args, **kwargs):
        """
        :param type[BaseClient] client_class:
        """
        client = client_class(*args, **kwargs)

        if self.ps_client_name is not None:
            client.ps_client_name = self.ps_client_name

        return client


class JobArtifactsDownloader(ResourceDownloader):
    CLIENT_CLASS = JobsClient

    def _get_files_list(self, job_id):
        files = self.client.artifacts_list(job_id)
        files = tuple((f.file, f.url) for f in files)
        return files


class ModelFilesDownloader(ResourceDownloader):
    CLIENT_CLASS = ModelsClient

    def _get_files_list(self, model_id):
        files = self.client.get_model_files(model_id=model_id, links=True)
        files = tuple((f.file, f.url) for f in files)
        return files
