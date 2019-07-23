import pydoc

import terminaltables
from click import style
from halo import halo

from gradient import logger, api_sdk, exceptions
from gradient.api_sdk.utils import print_dict_recursive
from gradient.commands import common
from gradient.exceptions import BadResponseError
from gradient.utils import get_terminal_lines
from gradient.workspace import MultipartEncoder, WorkspaceHandler


class JobsCommandBase(object):
    def __init__(self, job_client, logger_=logger.Logger()):
        self.job_client = job_client
        self.logger = logger_

    def _log_message(self, response, success_msg_template, error_msg):
        if response.ok:
            try:
                handle = response.json()
            except (ValueError, KeyError):
                self.logger.log(success_msg_template)
            else:
                msg = success_msg_template.format(**handle)
                self.logger.log(msg)
        else:
            try:
                data = response.json()
                self.logger.log_error_response(data)
            except ValueError:
                self.logger.error(error_msg)


class DeleteJobCommand(JobsCommandBase):

    def execute(self, job_id):
        response = self.job_client.delete(job_id)
        self._log_message(response,
                          "Job deleted",
                          "Unknown error while deleting job")


class StopJobCommand(JobsCommandBase):

    def execute(self, job_id):
        response = self.job_client.dtop(job_id)
        self._log_message(response,
                          "Job stopped",
                          "Unknown error while stopping job")


class ListJobsCommand(JobsCommandBase):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, **kwargs):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instances = self._get_instances(**kwargs)

        self._log_objects_list(instances)

    def _get_instances(self, **kwargs):
        filters = self._get_request_json(kwargs)

        try:
            instances = self.job_client.list(filters)
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
        response = self.job_client.get(self.request_url, json=json_, params=params)
        return response

    @staticmethod
    def _make_table(table_data):
        ascii_table = terminaltables.AsciiTable(table_data)
        table_string = ascii_table.table
        return table_string


class JobLogsCommand(JobsCommandBase):

    def execute(self, job_id, line, limit, follow):
        if follow:
            self.logger.log("Awaiting logs...")
            self._log_logs_continuously(job_id, line, limit)
        else:
            self._log_table_of_logs(job_id, line, limit)

    def _log_table_of_logs(self, job_id, line, limit):
        logs = self.job_client.logs(job_id, line, limit)
        if not logs:
            self.logger.log("No logs found")
            return

        table_str = self._make_table(logs, job_id)
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

    def _log_logs_continuously(self, job_id, line, limit):
        logs_gen = self.job_client.yield_logs(job_id, line, limit)
        for log in logs_gen:
            log_msg = "{}\t{}\t{}".format(*self._format_row(job_id, log))
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


class CreateJobCommand(JobsCommandBase):

    def execute(self, json_):
        url = "/jobs/createJob/"
        data = None
        self.set_project_if_not_provided(json_)

        workspace_url = self._workspace_handler.handle(json_)
        if workspace_url:
            if self._workspace_handler.archive_path:
                data = self._get_multipart_data(json_)
            else:
                json_["workspaceFileName"] = workspace_url

        json_.pop("workspaceArchive", None)
        json_.pop("workspaceUrl", None)
        json_.pop("workspace", None)
        if workspace_url:
            if workspace_url != "none":
                json_["workspaceUrl"] = workspace_url
            else:
                json_["workspace"] = workspace_url

        self.logger.log("Creating job...")
        response = self.job_client.create(json_)
        self._log_message(response,
                          "Job created - ID: {id}",
                          "Unknown error while creating job")


class ArtifactsDestroyCommand(JobsCommandBase):
    def execute(self, job_id, files=None):
        url = '/jobs/{}/artifactsDestroy'.format(job_id)
        params = None
        if files:
            params = {'files': files}
        response = self.api.post(url, params=params)
        self._log_message(response, "Artifacts destroyed", "Unknown error while destroying artifacts")


class ArtifactsGetCommand(JobsCommandBase):
    def execute(self, job_id):
        url = '/jobs/artifactsGet'
        response = self.api.get(url, params={'jobId': job_id})

        self._log_artifacts(response)

    def _log_artifacts(self, response):
        try:
            artifacts_json = response.json()
            if response.ok:
                print_dict_recursive(artifacts_json, self.logger)
            else:
                raise BadResponseError(
                    '{}: {}'.format(artifacts_json['error']['status'], artifacts_json['error']['message']))
        except (ValueError, KeyError, BadResponseError) as e:
            self.logger.error("Error occurred while getting artifacts: {}".format(str(e)))


class ArtifactsListCommand(common.ListCommand):
    kwargs = {}

    def execute(self, **kwargs):
        self.kwargs = kwargs
        return super(ArtifactsListCommand, self).execute(**kwargs)

    @property
    def request_url(self):
        return '/jobs/artifactsList'

    def _get_request_params(self, kwargs):
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
