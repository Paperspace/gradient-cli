from .common import BaseRepository, ListResources, GetResource
from .. import config, serializers
from ..clients import http_client


class WorkflowsMixin(object):
    SERIALIZER_CLS = serializers.WorkflowSchema

    @staticmethod
    def _get_api_url(**kwargs):
        return config.config.CONFIG_HOST


class ListWorkflows(WorkflowsMixin, ListResources):
    def get_request_url(self, **kwargs):
        return "/workflows"

    def _get_instances(self, response, **kwargs):
        if not response.data:
            return []

        objects = self._parse_objects(response.data, **kwargs)
        return objects

class GetWorkflow(WorkflowsMixin, BaseRepository):
    def get_request_url(self, **kwargs):
        return "/workflows/{}".format(kwargs.get("id"))

    def get(self, **kwargs):
        json_ = self._get_request_json(kwargs)
        params = self._get_request_params(kwargs)
        url = self.get_request_url(**kwargs)
        client = self._get_client(**kwargs)
        response = self._send_request(client, url, json=json_, params=params)
        gradient_response = http_client.GradientResponse.interpret_response(response)

        if not gradient_response.data:
            return {}

        return gradient_response.data


class WorkflowRunsMixin(object):
    @staticmethod
    def _get_api_url(**kwargs):
        return config.config.CONFIG_HOST

class ListWorkflowRuns(WorkflowRunsMixin, BaseRepository):
    @staticmethod
    def _get_api_url(**kwargs):
        return config.config.CONFIG_HOST


    def get_request_url(self, **kwargs):
        return "/workflows/{}/runs".format(kwargs.get("id"))

    def get(self, **kwargs):
        json_ = self._get_request_json(kwargs)
        params = self._get_request_params(kwargs)
        url = self.get_request_url(**kwargs)
        client = self._get_client(**kwargs)
        response = self._send_request(client, url, json=json_, params=params)
        gradient_response = http_client.GradientResponse.interpret_response(response)

        if not gradient_response.data:
            return []

        return gradient_response.data

class GetWorkflowRun(WorkflowRunsMixin, BaseRepository):
    def get_request_url(self, **kwargs):
        return "/workflows/{}/runs/{}".format(kwargs.get("id"), kwargs.get("run"))

    def get(self, **kwargs):
        json_ = self._get_request_json(kwargs)
        params = self._get_request_params(kwargs)
        url = self.get_request_url(**kwargs)
        client = self._get_client(**kwargs)
        response = self._send_request(client, url, json=json_, params=params)
        gradient_response = http_client.GradientResponse.interpret_response(response)

        if not gradient_response.data:
            return {}

        return gradient_response.data
