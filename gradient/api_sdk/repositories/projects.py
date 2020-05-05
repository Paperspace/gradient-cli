from .. import config
from .. import serializers
from ..repositories.common import CreateResource, ListResources, DeleteResource, GetResource
from ..sdk_exceptions import ResourceFetchingError


class GetBaseProjectsApiUrlMixin(object):
    def _get_api_url(self, **_):
        return config.config.CONFIG_HOST


class CreateProject(GetBaseProjectsApiUrlMixin, CreateResource):
    SERIALIZER_CLS = serializers.Project

    def get_request_url(self, **_):
        return "/projects/"


class ListProjects(GetBaseProjectsApiUrlMixin, ListResources):
    SERIALIZER_CLS = serializers.Project

    def get_request_url(self, **kwargs):
        return "/projects/"

    def _get_instance_dicts(self, data, **kwargs):
        project_dict_list = data["data"]
        return project_dict_list

    def _get_request_params(self, kwargs):
        params = {
            "filter": """{"offset":0,"where":{"dtDeleted":null},"order":"dtCreated desc"}"""
        }

        tags = kwargs.get("tags")
        if tags:
            params["tagFilter"] = tags

        return params


class DeleteProject(GetBaseProjectsApiUrlMixin, DeleteResource):
    def get_request_url(self, **kwargs):
        return "/projects/{}/deleteProject".format(kwargs.get("id"))

    def _send_request(self, client, url, json_data=None):
        response = client.post(url, json=json_data)
        return response


class GetProject(GetBaseProjectsApiUrlMixin, GetResource):
    SERIALIZER_CLS = serializers.Project

    def get_request_url(self, **kwargs):
        return "/projects/"

    def _get_request_params(self, kwargs):
        id_ = kwargs["id"]
        params = {
            "filter": """{"where":{"handle":"%s"}}""" % id_
        }

        return params

    def _parse_object(self, instance_dict, **kwargs):
        try:
            instance_dict = instance_dict["data"][0]
        except IndexError:
            raise ResourceFetchingError("Project not found")

        instance_dict = super(GetProject, self)._parse_object(instance_dict, **kwargs)
        return instance_dict
