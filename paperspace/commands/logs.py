import pydoc

import terminaltables
from colorclass import Color

from paperspace.commands import CommandBase
from paperspace.utils import get_terminal_lines


class ListLogsCommand(CommandBase):
    last_line_number = 0
    base_url = "/jobs/logs?jobId={}&line={}"

    is_logs_complete = False

    def execute(self, job_id):
        table_data = [("LINE", "MESSAGE")]
        table = terminaltables.AsciiTable(table_data, title=f"Job {job_id} logs")

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
            table_data.append((Color.colorize("red", log.get("line")), log.get("message")))

        return table.table
