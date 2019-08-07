import abc
import pydoc

import six
import terminaltables
from click import style
from halo import halo

from gradient import api_sdk, exceptions
from gradient.api_sdk.utils import print_dict_recursive
from gradient.commands.common import BaseCommand
from gradient.exceptions import BadResponseError
from gradient.utils import get_terminal_lines
from gradient.workspace import MultipartEncoder


@six.add_metaclass(abc.ABCMeta)
class BaseJobCommand(BaseCommand):
    def _get_client(self, api_key, logger_):
        client = api_sdk.clients.JobsClient(api_key=api_key, logger=logger_)
        return client

    def _log_message(self, response_data, is_response_ok, success_msg_template, error_msg):
        if is_response_ok:
            try:
                handle = response_data
            except (ValueError, KeyError):
                self.logger.log(success_msg_template)
            else:
                msg = success_msg_template.format(**handle)
                self.logger.log(msg)
        else:
            try:
                data = response_data
                self.logger.log_error_response(data)
            except ValueError:
                self.logger.error(error_msg)


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
        self.client.client.headers["Content-Type"] = monitor.content_type
        data = monitor
        return data

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
        filters = self._get_request_json(kwargs)

        try:
            instances = self.client.list(filters)
        except api_sdk.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instances

    @property
    def request_url(self):
        return "/jobs/getJobs/"

    @staticmethod
    def _get_request_json(kwargs):
        filters = kwargs.get("filters")
        json_ = filters or None
        return json_

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
    def _get_objects(response, kwargs):
        data = response.json()
        return data

    def _get_response(self, kwargs):
        json_ = self._get_request_json(kwargs)
        params = self._get_request_params(kwargs)
        response = self.client.get(self.request_url, json=json_, params=params)
        return response

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


class ArtifactsDestroyCommand(BaseJobCommand):
    def execute(self, job_id, files=None):
        params = None
        if files:
            params = {"files": files}

        self.client.artifacts_delete(job_id, params)
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
            instances = self._get_instances(**kwargs)

        self._log_objects_list(instances)

    def _get_instances(self, **kwargs):
        filters = self._get_request_params(kwargs)

        try:
            instances = self.client.artifacts_list(filters)
        except api_sdk.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instances

    @staticmethod
    def _get_request_params(kwargs):
        params = {'jobId': kwargs['job_id']}

        files = kwargs.get('files')
        if files:
            params['files'] = files
        size = kwargs.get('size', False)
        if size:
            params['size'] = size
        links = kwargs.get('links', False)
        if links:
            params['links'] = links

        return params

    def _get_table_data(self, artifacts):
        columns = ['Files']
        if self.kwargs.get('size'):
            columns.append('Size (in bytes)')
        if self.kwargs.get('links'):
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
