import json

from .common import CreateResource, DeleteResource, ListResources, GetResource, GetMetrics, StreamMetrics
from .. import config
from .. import serializers, sdk_exceptions


class GetNotebookApiUrlMixin(object):
    def _get_api_url(self, **kwargs):
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
        url = "notebooks/getNotebook"
        return url

    def _parse_object(self, data, **kwargs):
        # this ugly hack is here because marshmallow disallows reading value into `id` field
        # if JSON's field was named differently (despite using load_from in schema definition)
        data["id"] = data["handle"]

        serializer = serializers.NotebookSchema()
        notebooks = serializer.get_instance(data)
        return notebooks

    def _get_request_json(self, kwargs):
        notebook_id = kwargs["id"]
        j = {"notebookId": notebook_id}
        return j


class ListNotebooks(GetNotebookApiUrlMixin, ListResources):
    def get_request_url(self, **kwargs):
        return "notebooks/getNotebooks"

    def _get_meta_data(self, resp, **kwargs):
        metadata = {
            "total": resp.data.get("total"),
            "runningTotal": resp.data.get("runningTotal"),
            "freeTierRunningTotal": resp.data.get("freeTierRunningTotal"),
            "displayTotal": resp.data.get("displayTotal"),
        }
        return metadata

    def _parse_objects(self, data, **kwargs):
        notebook_dicts = data["notebookList"]
        # this ugly hack is here because marshmallow disallows reading value into `id` field
        # if JSON's field was named differently (despite using load_from in schema definition)
        for d in notebook_dicts:
            d["id"] = d["handle"]

        serializer = serializers.NotebookSchema()
        notebooks = serializer.get_instance(notebook_dicts, many=True)
        return notebooks

    def _get_request_params(self, kwargs):
        filters = {
            "filter": {
                "limit": kwargs.get("limit"),
                "offset": kwargs.get("offset"),
                "where": {
                    "dtDeleted": None,
                },
                "order": "jobId desc",
            },
        }

        params = {}
        filter_string = json.dumps(filters)
        params["filter"] = filter_string

        tags = kwargs.get("tags", [])
        for i, tag in enumerate(tags):
            key = "tagFilter[{}]".format(i)
            params[key] = tag

        return params


class GetNotebookMetrics(GetMetrics):
    OBJECT_TYPE = "notebook"

    def _get_instance_by_id(self, instance_id, **kwargs):
        repository = GetNotebook(self.api_key, logger=self.logger, ps_client_name=self.ps_client_name)
        instance = repository.get(id=instance_id)
        return instance

    def _get_start_date(self, instance, kwargs):
        rv = super(GetNotebookMetrics, self)._get_start_date(instance, kwargs)
        if rv is None:
            raise sdk_exceptions.GradientSdkError("Notebook has not started yet")

        return rv


class StreamNotebookMetrics(StreamMetrics):
    OBJECT_TYPE = "notebook"

    def _get_metrics_api_url(self, instance_id, protocol="https"):
        repository = GetNotebook(api_key=self.api_key, logger=self.logger, ps_client_name=self.ps_client_name)
        deployment = repository.get(id=instance_id)

        metrics_api_url = super(StreamNotebookMetrics, self)._get_metrics_api_url(deployment, protocol="wss")
        return metrics_api_url
