import abc
import pydoc

import six
import terminaltables
from click import style
from halo import halo

from gradient import api_sdk, exceptions, Job, config
from gradient.api_sdk.clients import http_client
from gradient.api_sdk.clients.base_client import BaseClient
from gradient.api_sdk.repositories.jobs import RunJob
from gradient.api_sdk.utils import print_dict_recursive
from gradient.commands.common import BaseCommand
from gradient.utils import get_terminal_lines
from gradient.workspace import MultipartEncoder


@six.add_metaclass(abc.ABCMeta)
class BaseJobCommand(BaseCommand):
    def _get_client(self, api_key, logger_):
        client = api_sdk.clients.JobsClient(api_key=api_key, logger=logger_)
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
            try:
                job_id = self._create(json_, data)
            except api_sdk.GradientSdkError as e:
                self.logger.error(e)
                return

        self.logger.log(self.CREATE_SUCCESS_MESSAGE_TEMPLATE.format(job_id))

    def _handle_workspace(self, instance_dict):
        """

        :param instance_dict:
        :return:
        """
        data = None

        self._set_project_if_not_provided(instance_dict)
        workspace_url = self.workspace_handler.handle(instance_dict)
        if workspace_url:
            if self.workspace_handler.archive_path:
                data = self._get_multipart_data(instance_dict)
            else:
                instance_dict["workspace_file_name"] = workspace_url

        return instance_dict, data

    def _get_multipart_data(self, json_):
        archive_basename = self.workspace_handler.archive_basename
        json_["workspace_file_name"] = archive_basename
        job_data = self._get_files_dict(archive_basename)
        monitor = MultipartEncoder(job_data).get_monitor()
        return monitor

    def _get_files_dict(self, archive_basename):
        job_data = {'file': (archive_basename, open(self.workspace_handler.archive_path, 'rb'), 'text/plain')}
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
        except api_sdk.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instances

    @staticmethod
    def _get_table_data(jobs):
        data = [("ID", "Name", "Project", "Cluster", "Machine Type", "Created")]
        for job in jobs:
            id_ = job.id_
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


class JobLogsCommand(BaseJobCommand):

    def execute(self, job_id, line, limit, follow):
        if follow:
            self.logger.log("Awaiting logs...")
            self._log_logs_continuously(job_id, line, limit)
        else:
            self._log_table_of_logs(job_id, line, limit)

    def _log_table_of_logs(self, job_id, line, limit):
        logs = self.client.logs(job_id, line, limit)
        if not logs:
            self.logger.log("No logs found")
            return

        table_str = self._make_table(logs, job_id)
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

    def _log_logs_continuously(self, job_id, line, limit):
        logs_gen = self.client.yield_logs(job_id, line, limit)
        for log in logs_gen:
            log_msg = "{}\t{}".format(*self._format_row(log))
            self.logger.log(log_msg)

    @staticmethod
    def _format_row(log_row):
        return (style(fg="red", text=str(log_row.line)),
                log_row.message)

    def _make_table(self, logs, job_id):
        table_title = "Job %s logs" % job_id
        table_data = [("LINE", "MESSAGE")]
        table = terminaltables.AsciiTable(table_data, title=table_title)

        for log in logs:
            table_data.append(self._format_row(log))

        return table.table


class CreateJobCommand(BaseCreateJobCommandMixin, BaseJobCommand):

    def _create(self, json_, data):
        return self.client.create(data=data, **json_)


class JobRunClient(BaseClient):
    def __init__(self, http_client_, *args, **kwargs):
        super(JobRunClient, self).__init__(*args, **kwargs)
        self.client = http_client_

    def create(
            self,
            machine_type,
            container,
            project_id,
            data=None,
            name=None,
            command=None,
            ports=None,
            is_public=None,
            workspace=None,
            workspace_archive=None,
            workspace_url=None,
            working_directory=None,
            ignore_files=None,
            experiment_id=None,
            job_env=None,
            use_dockerfile=None,
            is_preemptible=None,
            project=None,
            started_by_user_id=None,
            rel_dockerfile_path=None,
            registry_username=None,
            registry_password=None,
            cluster=None,
            cluster_id=None,
            node_attrs=None,
            workspace_file_name=None,
    ):
        job = Job(
            machine_type=machine_type,
            container=container,
            project_id=project_id,
            name=name,
            command=command,
            ports=ports,
            is_public=is_public,
            workspace=workspace,
            workspace_archive=workspace_archive,
            workspace_url=workspace_url,
            working_directory=working_directory,
            ignore_files=ignore_files,
            experiment_id=experiment_id,
            job_env=job_env,
            use_dockerfile=use_dockerfile,
            is_preemptible=is_preemptible,
            project=project,
            started_by_user_id=started_by_user_id,
            rel_dockerfile_path=rel_dockerfile_path,
            registry_username=registry_username,
            registry_password=registry_password,
            cluster=cluster,
            cluster_id=cluster_id,
            target_node_attrs=node_attrs,
            workspace_file_name=workspace_file_name,
        )
        handle = RunJob(self.api_key, self.logger, self.client).create(job, data=data)
        return handle


class RunJobCommand(CreateJobCommand):
    def _get_client(self, api_key, logger_):
        if hasattr(self, "client"):
            return self.client

        http_client_ = http_client.API(config.config.CONFIG_HOST, api_key=api_key, logger=logger_)
        client = JobRunClient(http_client_, logger_, http_client_)
        return client


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
                instances = self.client.artifacts_list(**kwargs)
            except api_sdk.GradientSdkError as e:
                raise exceptions.ReceivingDataFailedError(e)

        self._log_objects_list(instances, kwargs)

    def _get_table_data(self, artifacts, kwargs):
        columns = ['Files']
        if kwargs.get('size'):
            columns.append('Size (in bytes)')
        if kwargs.get('links'):
            columns.append('URL')

        data = [tuple(columns)]
        for artifact in artifacts:
            row = [artifact.get('file')]
            if 'size' in artifact.keys():
                row.append(artifact['size'])
            if 'url' in artifact.keys():
                row.append(artifact['url'])
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
