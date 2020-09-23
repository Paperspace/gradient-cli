import abc
import json
import os
import pydoc

import six
import terminaltables
from halo import halo

from gradient import api_sdk, exceptions, JobArtifactsDownloader, cli_constants
from gradient.api_sdk import config, sdk_exceptions
from gradient.api_sdk import utils
from gradient.api_sdk.clients import http_client
from gradient.api_sdk.utils import print_dict_recursive, concatenate_urls, MultipartEncoder
from gradient.cliutils import get_terminal_lines
from gradient.commands.common import BaseCommand, StreamMetricsCommand, LogsCommandMixin


@six.add_metaclass(abc.ABCMeta)
class BaseJobCommand(BaseCommand):
    def _get_client(self, api_key, logger_):
        client = api_sdk.clients.JobsClient(
            api_key=api_key,
            logger=logger_,
            ps_client_name=cli_constants.CLI_PS_CLIENT_NAME,
        )
        return client


@six.add_metaclass(abc.ABCMeta)
class BaseCreateJobCommandMixin(object):
    SPINNER_MESSAGE = "Creating new job"
    CREATE_SUCCESS_MESSAGE_TEMPLATE = "New job created with ID: {}"

    def __init__(self, workspace_handler, *args, **kwargs):
        super(BaseCreateJobCommandMixin, self).__init__(*args, **kwargs)
        self.workspace_handler = workspace_handler

    def execute(self, json_):
        json_, data = self._handle_workspace(json_)

        with halo.Halo(text=self.SPINNER_MESSAGE, spinner="dots"):
            job_id = self._create(json_, data)

        self.logger.log(self.CREATE_SUCCESS_MESSAGE_TEMPLATE.format(job_id))
        self.logger.log(self.get_instance_url(job_id))

    @staticmethod
    def get_instance_url(instance_id):
        url = concatenate_urls(config.config.WEB_URL, "jobs/{}".format(instance_id))
        return url

    def _handle_workspace(self, instance_dict):
        """

        :param instance_dict:
        :return:
        """
        data = None

        self._set_project_if_not_provided(instance_dict)
        workspace_url = self.workspace_handler.handle(instance_dict)
        if workspace_url:
            if utils.PathParser.is_local_zip_file(workspace_url):
                data = self._get_multipart_data(workspace_url, instance_dict)
            else:
                instance_dict["workspace_file_name"] = workspace_url

        return instance_dict, data

    def _get_multipart_data(self, workspace_url, json_):
        archive_basename = os.path.basename(workspace_url)
        json_["workspace_file_name"] = archive_basename
        job_data = self._get_files_dict(workspace_url, archive_basename)
        monitor = MultipartEncoder(job_data).get_monitor()
        return monitor

    def _get_files_dict(self, workspace_url, archive_basename):
        job_data = {'file': (archive_basename, open(workspace_url, 'rb'), 'text/plain')}
        return job_data

    @staticmethod
    def _set_project_if_not_provided(json_):
        if not json_.get("project_id"):
            json_["project"] = "gradient-project"

    @abc.abstractmethod
    def _create(self, json_, data):
        pass


class DeleteJobCommand(BaseJobCommand):

    def execute(self, job_id):
        self.client.delete(job_id)
        self.logger.log("Job {} deleted".format(job_id))


class StopJobCommand(BaseJobCommand):

    def execute(self, job_id):
        self.client.stop(job_id)
        self.logger.log("Job {} stopped".format(job_id))


class ListJobsCommand(BaseJobCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, **kwargs):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instances = self._get_instances(**kwargs)

        self._log_objects_list(instances)

    def _get_instances(self, **kwargs):

        try:
            instances = self.client.list(**kwargs)
        except sdk_exceptions.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instances

    @staticmethod
    def _get_table_data(jobs):
        data = [("ID", "Name", "Project", "Cluster", "Machine Type", "Created")]
        for job in jobs:
            id_ = job.id
            name = job.name
            project = job.project
            cluster = job.cluster
            machine_type = job.machine_type
            created = job.dt_created
            data.append((id_, name, project, cluster, machine_type, created))

        return data

    def _log_objects_list(self, objects):
        if not objects:
            self.logger.warning("No data found")
            return

        table_data = self._get_table_data(objects)
        table_str = self._make_table(table_data)
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

    @staticmethod
    def _make_table(table_data):
        ascii_table = terminaltables.AsciiTable(table_data)
        table_string = ascii_table.table
        return table_string


class JobLogsCommand(LogsCommandMixin, BaseJobCommand):
    ENTITY = "Job"


class CreateJobCommand(BaseCreateJobCommandMixin, BaseJobCommand):

    def _create(self, json_, data):
        # because ignore_files is used by workspace handlers and not needed anymore (will fail if not "popped")
        json_.pop("ignore_files", None)
        json_.pop("workspace", None)

        return self.client.create(data=data, **json_)


class ArtifactsDestroyCommand(BaseJobCommand):
    def execute(self, job_id, files=None):
        self.client.artifacts_delete(job_id, files)
        self.logger.log("Job {} artifacts deleted".format(job_id))


class ArtifactsGetCommand(BaseJobCommand):
    def execute(self, job_id):
        artifact = self.client.artifacts_get(job_id)

        self._log_artifacts(artifact, job_id)

    def _log_artifacts(self, artifact, job_id):
        if artifact:
            print_dict_recursive(artifact, self.logger)
        else:
            self.logger.log("No artifacts found for job {}".format(job_id))


class ArtifactsListCommand(BaseJobCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, **kwargs):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            try:
                start_after = None
                instances = []
                while True:
                    pagination_response = self.client.artifacts_list(start_after=start_after, **kwargs)

                    if pagination_response.data:
                        instances.extend(pagination_response.data)
                    start_after = pagination_response.start_after

                    if start_after is None:
                        break
            except sdk_exceptions.GradientSdkError as e:
                raise exceptions.ReceivingDataFailedError(e)

        self._log_objects_list(instances, kwargs)

    def _get_table_data(self, artifacts, kwargs):
        columns = ['Files']

        show_size = "size" in kwargs
        show_url = "url" in kwargs

        if show_size:
            columns.append('Size (in bytes)')
        if show_url:
            columns.append('URL')

        data = [tuple(columns)]
        for artifact in artifacts:
            row = [artifact.file]
            if show_size:
                row.append(artifact.size)
            if show_url:
                row.append(artifact.url)
            data.append(tuple(row))
        return data

    def _log_objects_list(self, objects, kwargs):
        if not objects:
            self.logger.warning("No data found")
            return

        table_data = self._get_table_data(objects, kwargs)
        table_str = self._make_table(table_data)
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

    @staticmethod
    def _make_table(table_data):
        ascii_table = terminaltables.AsciiTable(table_data)
        table_string = ascii_table.table
        return table_string


class DownloadArtifactsCommand(BaseJobCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, job_id, destination_directory):
        artifact_downloader = JobArtifactsDownloader(
            self.api_key,
            logger=self.logger,
            ps_client_name=cli_constants.CLI_PS_CLIENT_NAME,
        )
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            try:
                artifact_downloader.download(job_id, destination_directory)
            except OSError as e:
                raise sdk_exceptions.GradientSdkError(e)


class JobAddTagsCommand(BaseJobCommand):
    def execute(self, job_id, *args, **kwargs):
        self.client.add_tags(job_id, **kwargs)
        self.logger.log("Tags added to job")


class JobRemoveTagsCommand(BaseJobCommand):
    def execute(self, job_id, *args, **kwargs):
        self.client.remove_tags(job_id, **kwargs)
        self.logger.log("Tags removed from job")


class GetJobMetricsCommand(BaseJobCommand):
    def execute(self, deployment_id, start, end, interval, built_in_metrics, *args, **kwargs):
        metrics = self.client.get_metrics(
            deployment_id,
            start=start,
            end=end,
            built_in_metrics=built_in_metrics,
            interval=interval,
        )
        formatted_metrics = json.dumps(metrics, indent=2, sort_keys=True)
        self.logger.log(formatted_metrics)


class StreamJobMetricsCommand(StreamMetricsCommand, BaseJobCommand):
    pass
