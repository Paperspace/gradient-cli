from gradient import config
from .common import ListResources, CreateResource, StartResource, StopResource
from .. import serializers


class GetBaseDeploymentApiUrlMixin(object):
    def _get_api_url(self, **_):
        return config.config.CONFIG_HOST


class ListDeployments(GetBaseDeploymentApiUrlMixin, ListResources):
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
        filters = {}
        if kwargs["model_id"]:
            filters["modelId"] = kwargs["model_id"]

        if kwargs["state"]:
            filters["state"] = kwargs["state"]

        if kwargs["project_id"]:
            filters["projectId"] = kwargs["project_id"]

        if not filters:
            return None

        json_ = {"filter": {"where": {"and": [filters]}}}
        return json_


class CreateDeployment(GetBaseDeploymentApiUrlMixin, CreateResource):
    SERIALIZER_CLS = serializers.DeploymentSchema

    def get_request_url(self, **kwargs):
        if kwargs.get("use_vpc") or config.config.USE_VPC:
            return "/deployments/v2/createDeployment/"

        return "/deployments/createDeployment/"

    def _get_id_from_response(self, response):
        handle = response.data["deployment"]["id"]
        return handle


class StartDeployment(GetBaseDeploymentApiUrlMixin, StartResource):
    def get_request_url(self, **kwargs):
        if kwargs.get("use_vpc") or config.config.USE_VPC:
            return "/deployments/v2/updateDeployment/"

        return "/deployments/updateDeployment/"

    def _get_request_json(self, kwargs):
        data = {
            "id": kwargs["id"],
            "isRunning": True,
        }
        return data

    def _send_request(self, client, url, json_data=None):
        response = client.post(url, json=json_data)
        return response


class StopDeployment(GetBaseDeploymentApiUrlMixin, StopResource):
    def get_request_url(self, **kwargs):
        if kwargs.get("use_vpc") or config.config.USE_VPC:
            return "/deployments/v2/updateDeployment/"

        return "/deployments/updateDeployment/"

    def _get_request_json(self, kwargs):
        data = {
            "id": kwargs["id"],
            "isRunning": False,
        }
        return data

    def _send_request(self, client, url, json_data=None):
        response = client.post(url, json=json_data)
        return response
