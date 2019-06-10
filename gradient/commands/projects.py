from gradient.commands import common


class ListProjectsCommand(common.ListCommand):
    @property
    def request_url(self):
        return "/projects/"

    def _get_request_json(self, kwargs):
        # TODO: PS_API should not require teamId but it does now, delete teamId from json when PS_API is fixed
        return {"teamId": 666}

    def _get_objects(self, response, kwargs):
        data = super(ListProjectsCommand, self)._get_objects(response, kwargs)
        objects = data["data"]
        return objects

    def _get_table_data(self, projects):
        data = [("ID", "Name", "Repository", "Created")]
        for project in projects:
            id_ = project.get("handle")
            name = project.get("name")
            repo_url = project.get("repoUrl")
            created = project.get("dtCreated")
            data.append((id_, name, repo_url, created))

        return data


class ProjectCommandBase(common.CommandBase):
    def _log_message(self, response, success_msg_template, error_msg):
        if response.ok:
            try:
                j = response.json()
            except (ValueError, KeyError):
                self.logger.error(success_msg_template)
            else:
                msg = success_msg_template.format(**j)
                self.logger.log(msg)
        else:
            try:
                data = response.json()
                self.logger.log_error_response(data)
            except ValueError:
                self.logger.error(error_msg)


class CreateProjectCommand(ProjectCommandBase):
    def execute(self, project):
        # TODO: remove the `project["teamId"] = "0"` once the API does not require it anymore
        # this is necessary since the API still requires the teamId but does not use it anymore
        project["teamId"] = "0"

        response = self.api.post("/projects/", json=project)

        self._log_message(response,
                          "Project created with ID: {handle}",
                          "Unknown error while creating new project")
