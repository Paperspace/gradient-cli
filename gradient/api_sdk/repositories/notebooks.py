from gradient import config
from .common import CreateResource, DeleteResource
from .. import serializers


class GetNotebookApiUrlMixin(object):
    def _get_api_url(self, use_vpc=False):
        return config.config.CONFIG_HOST


class CreateNotebook(GetNotebookApiUrlMixin, CreateResource):
    SERIALIZER_CLS = serializers.NotebookSchema

    def get_request_url(self, **kwargs):
        return "notebooks/createNotebook"

    def _process_instance_dict(self, instance_dict):
        # the API requires this field but marshmallow does not create it if it's value is None
        instance_dict.setdefault("containerId")
        return instance_dict


class DeleteNotebook(GetNotebookApiUrlMixin, DeleteResource):
    def get_request_url(self, **kwargs):
        return "notebooks/v2/deleteNotebook"

    def _get_request_json(self, kwargs):
        notebook_id = kwargs["id"]
        d = {"notebookId": notebook_id}
        return d

    def _send_request(self, client, url, json_data=None):
        response = client.post(url, json=json_data)
        return response
