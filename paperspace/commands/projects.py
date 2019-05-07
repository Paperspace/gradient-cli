import pydoc

import terminaltables

from paperspace import client, config, version, logger
from paperspace.utils import get_terminal_lines

default_headers = {"X-API-Key": config.PAPERSPACE_API_KEY,
                   "ps_client_name": "paperspace-python",
                   "ps_client_version": version.version}
deployments_api = client.API(config.CONFIG_HOST, headers=default_headers)


class ProjectsCommandBase(object):
    def __init__(self, api=deployments_api, logger_=logger):
        self.api = api
        self.logger = logger_


class ListProjectsCommand(ProjectsCommandBase):
    def execute(self):
        # TODO: PS_API should not require teamId but it does now, so change the following line
        # TODO: to `json_ = None` or whatever works when PS_API is fixed:
        json_ = {"teamId": 666}
        response = self.api.get("/projects/", json=json_)

        try:
            data = response.json()
            if not response.ok:
                self.logger.log_error_response(data)
                return
        except (ValueError, KeyError) as e:
            self.logger.error("Error while parsing response data: {}".format(e))
        else:
            self._log_projects_list(data)

    def _log_projects_list(self, data):
        if not data.get("data"):
            self.logger.warning("No projects found")
        else:
            table_str = self._make_table(data["data"])
            if len(table_str.splitlines()) > get_terminal_lines():
                pydoc.pager(table_str)
            else:
                self.logger.log(table_str)

    @staticmethod
    def _make_table(projects):
        data = [("ID", "Name", "Repository", "Created")]
        for project in projects:
            id_ = project.get("handle")
            name = project.get("name")
            repo_url = project.get("repoUrl")
            created = project.get("dtCreated")
            data.append((id_, name, repo_url, created))

        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string
