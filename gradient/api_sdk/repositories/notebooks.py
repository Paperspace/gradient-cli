import json

from ..clients import http_client
from ..sdk_exceptions import ResourceCreatingError
from .common import CreateResource, DeleteResource, ListResources, GetResource, \
    StopResource, GetMetrics, StreamMetrics, BaseRepository
from .. import config
from .. import serializers, sdk_exceptions


class GetNotebookApiUrlMixin(object):
    def _get_api_url(self, **kwargs):
        return config.config.CONFIG_HOST


class CreateNotebook(GetNotebookApiUrlMixin, CreateResource):
    SERIALIZER_CLS = serializers.NotebookSchema

    def get_request_url(self, **kwargs):
        return "notebooks/v2/createNotebook"


class StartNotebook(GetNotebookApiUrlMixin, CreateResource):
    SERIALIZER_CLS = serializers.NotebookStartSchema

    def start(self, instance, data=None, path=None):
        # notebook start is more like a create than a true start
        # as it posts and you need to send more data than just a
        # handle
        return self.create(instance, data=data, path=path)

    def get_request_url(self, **kwargs):
        return "notebooks/v2/startNotebook"


class ForkNotebook(GetNotebookApiUrlMixin, BaseRepository):
    SERIALIZER_CLS = serializers.NotebookSchema
    VALIDATION_ERROR_MESSAGE = "Failed to fork notebook"

    def fork(self, id):
        instance = {"notebookId": id}
        handle = self._send_request(instance)
        return handle

    def _process_response(self, response):
        try:
            return response.data["handle"]
        except Exception as e:
            raise ResourceCreatingError(e)


    def _send_request(self, data):
        url = self.get_request_url()
        client = self._get_client()
        response = client.post(url, json=data)
        gradient_response = http_client.GradientResponse.interpret_response(response)
        self._validate_response(gradient_response)
        handle = self._process_response(gradient_response)
        return handle

    def get_request_url(self, **kwargs):
        return "notebooks/v2/forkNotebook"


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

class StopNotebook(GetNotebookApiUrlMixin, StopResource):

    def get_request_url(self, **kwargs):
        return "notebooks/v2/stopNotebook"

    def _get_request_json(self, kwargs):
        notebook_id = kwargs["id"]
        d = {"notebookId": notebook_id}
        return d

    def _send_request(self, client, url, json_data=None):
        response = client.post(url, json=json_data)
        return response



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


class ListNotebookArtifacts(GetNotebookApiUrlMixin, ListResources):
    def _parse_objects(self, data, **kwargs):
        serializer = serializers.ArtifactSchema()
        files = serializer.get_instance(data, many=True)
        return files

    def get_request_url(self, **kwargs):
        return "/notebooks/artifactsList"

    def _get_request_params(self, kwargs):
        params = {
            "notebookId": kwargs.get("notebook_id"),
        }

        if kwargs.get("files"):
            params["files"] = kwargs.get("files")

        if kwargs.get("size"):
            params["size"] = kwargs.get("size")

        if kwargs.get("links"):
            params["links"] = kwargs.get("links")

        return params

