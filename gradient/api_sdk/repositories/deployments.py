from gradient.api_sdk.exceptions import ResourceFetchingError
from gradient.api_sdk.utils import MessageExtractor
from .common import ListResources, CreateResource, BaseRepository
from .. import serializers


class ListDeployments(ListResources):
    def get_request_url(self, **kwargs):
        return "/deployments/getDeploymentList/"

    def _parse_objects(self, data, **kwargs):
        deployment_dicts = self._get_deployments_dicts_from_json_data(data, kwargs)
        deployments = []

        for deployment_dict in deployment_dicts:
            deployment = serializers.DeploymentSchema().get_instance(deployment_dict)
            deployments.append(deployment)

        return deployments

    @staticmethod
    def _get_deployments_dicts_from_json_data(data, kwargs):
        return data["deploymentList"]

    def _get_request_json(self, kwargs):
        filters = dict()

        if kwargs.get("state"):
            filters["state"] = kwargs.get("state")

        if kwargs.get("project_id"):
            filters["projectId"] = kwargs.get("project_id")

        if kwargs.get("model_id"):
            filters["modelId"] = kwargs.get("model_id")

        if not filters:
            return None

        json_ = {"filter": {"where": {"and": [filters]}}}
        return json_


class CreateDeployment(CreateResource):

    SERIALIZER_CLS = serializers.DeploymentSchema

    def _get_create_url(self):
        return "/deployments/createDeployment/"

    def _get_id_from_response(self, response):
        handle = response.data["deployment"]["id"]
        return handle


class StartStopDeployment(BaseRepository):

    def get_request_url(self, **kwargs):
        return "/deployments/updateDeployment/"

    def start(self, deployment_id, is_running=True):
        url = self.get_request_url()
        kwargs = {"deployment_id": deployment_id, "is_running": is_running}
        json_ = self._get_request_json(kwargs)
        response = self.client.post(url, json=json_)
        self._validate_response(response)

    def _get_request_json(self, kwargs):
        return {
            "id": kwargs.get("deployment_id"),
            "isRunning": kwargs.get("is_running")
        }

    def _validate_response(self, response):
        if not response.ok:
            errors = MessageExtractor().get_message_from_response_data(response.json())
            raise ResourceFetchingError(errors)
