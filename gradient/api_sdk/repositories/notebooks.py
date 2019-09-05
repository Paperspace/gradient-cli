from gradient import config
from .common import CreateResource, DeleteResource, ListResources, GetResource
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


class GetNotebook(GetNotebookApiUrlMixin, GetResource):
    def get_request_url(self, **kwargs):
        notebook_id = kwargs["id"]
        url = "notebooks/{}/getNotebook".format(notebook_id)
        return url

    def _parse_object(self, data, **kwargs):
        # this ugly hack is here because marshmallow disallows reading value into `id` field
        # if JSON's field was named differently (despite using load_from in schema definition)
        data["id"] = data["handle"]

        serializer = serializers.NotebookSchema()
        notebooks = serializer.get_instance(data)
        return notebooks


class ListNotebooks(GetNotebookApiUrlMixin, ListResources):
    def get_request_url(self, **kwargs):
        return "notebooks/getNotebooks"

    def _parse_objects(self, data, **kwargs):
        notebook_dicts = data["notebookList"]
        # this ugly hack is here because marshmallow disallows reading value into `id` field
        # if JSON's field was named differently (despite using load_from in schema definition)
        for d in notebook_dicts:
            d["id"] = d["handle"]

        serializer = serializers.NotebookSchema()
        notebooks = serializer.get_instance(notebook_dicts, many=True)
        return notebooks

    def _get_request_json(self, kwargs):
        json_ = {
            "filter": {
                "filter": {
                    "limit": 11,
                    "offset": 0,
                    "where": {
                        "dtDeleted": None,
                    },
                    "order": "jobId desc",
                },
            },
        }
        return json_
