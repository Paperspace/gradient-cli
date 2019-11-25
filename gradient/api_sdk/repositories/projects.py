import gradient.api_sdk.config
from .. import serializers
from ..repositories.common import CreateResource, ListResources, DeleteResource


class GetBaseProjectsApiUrlMixin(object):
    def _get_api_url(self, **_):
        return gradient.api_sdk.config.config.CONFIG_HOST


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

    def _get_request_params(self, kwargs):
        filters = {
            "filter": """{"offset":0,"where":{"dtDeleted":null},"order":"dtCreated desc"}"""
        }
        return filters


class DeleteProject(GetBaseProjectsApiUrlMixin, DeleteResource):
    def get_request_url(self, **kwargs):
        return "/projects/{}/deleteProject".format(kwargs.get("id"))

    def _send_request(self, client, url, json_data=None):
        response = client.post(url, json=json_data)
        return response
