import pydoc

import terminaltables
from click import style

from paperspace import config, client
from paperspace.commands import common
from paperspace.exceptions import BadResponseError
from paperspace.utils import get_terminal_lines
from paperspace.workspace import S3WorkspaceHandler


class JobsCommandBase(common.CommandBase):
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
        url = "/jobs/{}/destroy/".format(job_id)
        response = self.api.post(url)
        self._log_message(response,
                          "Job deleted",
                          "Unknown error while deleting job")


class StopJobCommand(JobsCommandBase):
    def execute(self, job_id):
        url = "/jobs/{}/stop/".format(job_id)
        response = self.api.post(url)
        self._log_message(response,
                          "Job stopped",
                          "Unknown error while stopping job")


class ListJobsCommand(common.ListCommand):
    @property
    def request_url(self):
        return "/jobs/getJobs/"

    def _get_request_json(self, kwargs):
        filters = kwargs.get("filters")
        json_ = filters or None
        return json_

    def _get_table_data(self, jobs):
        data = [("ID", "Name", "Project", "Cluster", "Machine Type", "Created")]
        for job in jobs:
            id_ = job.get("id")
            name = job.get("name")
            project = job.get("project")
            cluster = job.get("cluster")
            machine_type = job.get("machineType")
            created = job.get("dtCreated")
            data.append((id_, name, project, cluster, machine_type, created))

        return data


class JobLogsCommand(common.CommandBase):
    last_line_number = 0
    base_url = "/jobs/logs?jobId={}&line={}"

    is_logs_complete = False

    def execute(self, job_id):
        table_title = "Job %s logs" % job_id
        table_data = [("LINE", "MESSAGE")]
        table = terminaltables.AsciiTable(table_data, title=table_title)

        while not self.is_logs_complete:
            response = self._get_logs(job_id)

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
                self._log_logs_list(data, table, table_data)

    def _get_logs(self, job_id):
        url = self.base_url.format(job_id, self.last_line_number)
        return self.api.get(url)

    def _log_logs_list(self, data, table, table_data):
        if not data:
            self.logger.log("No Logs found")
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
    def __init__(self, workspace_handler=None, **kwargs):
        super(CreateJobCommand, self).__init__(**kwargs)
        experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, api_key=kwargs.get('api_key'))
        self._workspace_handler = workspace_handler or S3WorkspaceHandler(experiments_api=experiments_api,
                                                                          logger=self.logger)

    def execute(self, json_):
        url = "/jobs/createJob/"

        workspace_url = self._workspace_handler.upload_workspace(json_)
        if workspace_url:
            json_['workspaceFileName'] = workspace_url
        json_['projectId'] = json_.get('projectId', json_.get('projectHandle'))
        response = self.api.post(url, json_)
        self._log_message(response,
                          "Job created",
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
                self._print_dict_recursive(artifacts_json)
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
