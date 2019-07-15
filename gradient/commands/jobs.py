import pydoc

import terminaltables
from click import style
from halo import halo

from gradient import logger, api_sdk, exceptions
from gradient.api_sdk.utils import print_dict_recursive
from gradient.commands import common
from gradient.exceptions import BadResponseError
from gradient.utils import get_terminal_lines


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


class JobLogsCommand(common.CommandBase):
    last_line_number = 0
    base_url = "/jobs/logs"

    is_logs_complete = False

    def execute(self, job_id, line, limit, follow):
        if follow:
            self.logger.log("Awaiting logs...")

        self.last_line_number = line
        table_title = "Job %s logs" % job_id
        table_data = [("LINE", "MESSAGE")]
        table = terminaltables.AsciiTable(table_data, title=table_title)

        while not self.is_logs_complete:
            response = self._get_logs(job_id, self.last_line_number, limit)

            try:
                data = response.json()
                if not response.ok:
                    self.logger.log_error_response(data)
                    return
            except (ValueError, KeyError) as e:
                if response.status_code == 204:
                    continue
                self.logger.log("Error while parsing response data: {}".format(e))
                return
            else:
                self._log_logs_list(data, table, table_data, follow)

            if not follow:
                self.is_logs_complete = True

    def _get_logs(self, job_id, line, limit):
        params = {
            'jobId': job_id,
            'line': line,
            'limit': limit
        }
        return self.api.get(self.base_url, params=params)

    def _log_logs_list(self, data, table, table_data, follow):
        if not data:
            self.logger.log("No Logs found")
            return
        if follow:
            if data[-1].get("message") == "PSEOF":
                self.is_logs_complete = True
            else:
                self.last_line_number = data[-1].get("line")
            for log in data:
                log_str = "{}\t{}\t{}"
                self.logger.log(log_str.format(style(fg="blue", text=str(log.get("jobId"))),
                                               style(fg="red", text=str(log.get("line"))), log.get("message")))
        else:
            table_str = self._make_table(data, table, table_data)
            if len(table_str.splitlines()) > get_terminal_lines():
                pydoc.pager(table_str)
            else:
                self.logger.log(table_str)

    def _make_table(self, logs, table, table_data):
        if logs[-1].get("message") == "PSEOF":
            self.is_logs_complete = True
        else:
            self.last_line_number = logs[-1].get("line")

        for log in logs:
            table_data.append((style(fg="red", text=str(log.get("line"))), log.get("message")))

        return table.table


class CreateJobCommand(JobsCommandBase):

    def execute(self, json_):
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
