from .common import BaseRepository, ListResources, GetResource, ListLogs
from .. import config, serializers
from ..clients import http_client
import json

class WorkflowsMixin(object):
    SERIALIZER_CLS = serializers.WorkflowSchema

    @staticmethod
    def _get_api_url(**kwargs):
        return config.config.CONFIG_HOST


class ListWorkflows(WorkflowsMixin, ListResources):
    def get_request_url(self, **kwargs):
        project_id = kwargs.get("project_id")
        if project_id is not None:
            return "/workflows?filter[where][projectId]={}".format(project_id)
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


class CreateWorkflow(WorkflowsMixin, BaseRepository):
    def get_request_url(self, **kwargs):
        return "/workflows"

    def _get_request_json(self, kwargs):
        return {"name": kwargs.get("name"), "projectId": kwargs.get("project_id")}

    def _send_request(self, client, url, json=None, params=None):
        response = client.post(url, json=json, params=params)
        return response

    def create(self, **kwargs):
        response = self._get(**kwargs)
        self._validate_response(response)

        if not response.data:
            return {}

        return response.data
        
class CreateWorkflowRun(WorkflowsMixin, BaseRepository):
    def get_request_url(self, **kwargs):
        return "/workflows/{}/runs".format(kwargs.get("id"))

    def _get_request_json(self, **kwargs):
        if kwargs.get("inputs") is not None:
            return {"spec": kwargs.get("spec"), "clusterId": kwargs.get("cluster_id"), "run": True, "markDefault": False, "inputs": kwargs.get("inputs") }

        return {"spec": kwargs.get("spec"), "clusterId": kwargs.get("cluster_id"), "run": True, "markDefault": False }

    def _send_create_request(self, **kwargs):
        url = self.get_request_url(**kwargs)
        client = self._get_client(**kwargs)
        json_ = self._get_request_json(**kwargs)

        response = client.post(url, json=json_)
        gradient_response = http_client.GradientResponse.interpret_response(response)
        json_formatted_str = json.dumps(gradient_response.data, indent=4)
        return gradient_response

    def create(self, **kwargs):
        response = self._send_create_request(**kwargs)
        self._validate_response(response)

        if not response.data:
            return {}

        return response.data

class ListWorkflowLogs(ListLogs):
    def _get_request_params(self, kwargs):
        params = {
            "jobId": kwargs["id"],
            "line": kwargs["line"],
            "limit": kwargs["limit"],
        }
        return params