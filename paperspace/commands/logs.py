from paperspace.commands import CommandBase


class LogsCommandBase(CommandBase):
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
                self.logger.log(error_msg)


class ListLogsCommand(LogsCommandBase):
    def execute(self, job_id):
        url = f"/jobs/logs?jobId={job_id}"
        response = self.api.get(url)
        self._log_message(
            response,
            "Job logs retrieved",
            "Unknown error while retrieving job logs"
        )
