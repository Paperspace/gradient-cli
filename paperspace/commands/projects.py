from paperspace.commands import common


class ListProjectsCommand(common.ListCommand):
    @property
    def request_url(self):
        return "/projects/"

    def _get_request_json(self, kwargs):
        # TODO: PS_API should not require teamId but it does now, delete this method when PS_API is fixed
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
