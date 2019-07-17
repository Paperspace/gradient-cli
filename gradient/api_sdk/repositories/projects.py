from .. import serializers
from ..repositories.common import CreateResource, ListResources


class CreateProject(CreateResource):
    SERIALIZER_CLS = serializers.Project

    def _get_create_url(self):
        return "/projects/"


class ListProjects(ListResources):
    def get_request_url(self, **kwargs):
        return "/projects/"

    def _parse_objects(self, data, **kwargs):
        project_dict_list = data["data"]
        projects = []
        for project_dict in project_dict_list:
            project = serializers.Project().get_instance(project_dict)
            projects.append(project)

        return projects
