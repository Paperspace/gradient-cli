from gradient import config
from .. import serializers
from ..repositories.common import CreateResource, ListResources


class GetBaseProjectsApiUrlMixin(object):
    def _get_api_url(self, **_):
        return config.config.CONFIG_HOST


class CreateProject(GetBaseProjectsApiUrlMixin, CreateResource):
    SERIALIZER_CLS = serializers.Project

    def get_request_url(self, **_):
        return "/projects/"


class ListProjects(GetBaseProjectsApiUrlMixin, ListResources):
    def get_request_url(self, **kwargs):
        return "/projects/"

    def _parse_objects(self, data, **kwargs):
        project_dict_list = data["data"]
        projects = []
        for project_dict in project_dict_list:
            project = serializers.Project().get_instance(project_dict)
            projects.append(project)

        return projects
