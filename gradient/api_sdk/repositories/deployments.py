from .common import ListResources, CreateResource
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
        filters = kwargs.get("filters")
        if not filters:
            return None

        json_ = filters
        return json_


class CreateDeployment(CreateResource):

    SERIALIZER_CLS = serializers.DeploymentSchema

    def _get_create_url(self):
        return "/deployments/createDeployment/"

    def _get_id_from_response(self, response):
        handle = response.data["deployment"]["id"]
        return handle


