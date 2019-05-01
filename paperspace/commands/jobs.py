import pydoc

import terminaltables

from paperspace.commands import CommandBase
from paperspace.utils import get_terminal_lines


class JobsCommandBase(CommandBase):
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


class ListJobsCommand(JobsCommandBase):
    def execute(self, filters=None):
        json_ = filters or None
        response = self.api.get("/jobs/getJobs/", json=json_)

        try:
            data = response.json()
            if not response.ok:
                self.logger.log_error_response(data)
                return
        except (ValueError, KeyError) as e:
            self.logger.error("Error while parsing response data: {}".format(e))
        else:
            self._log_jobs_list(data)

    def _log_jobs_list(self, data):
        if not data:
            self.logger.warning("No jobs found")
        else:
            table_str = self._make_table(data)
            if len(table_str.splitlines()) > get_terminal_lines():
                pydoc.pager(table_str)
            else:
                self.logger.log(table_str)

    @staticmethod
    def _make_table(jobs):
        data = [("ID", "Name", "Project", "Cluster", "Machine Type", "Created")]
        for job in jobs:
            id_ = job.get("id")
            name = job.get("name")
            project = job.get("project")
            cluster = job.get("cluster")
            machine_type = job.get("machineType")
            created = job.get("dtCreated")
            data.append((id_, name, project, cluster, machine_type, created))

        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string
