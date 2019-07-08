from .common import ListResources
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
        json_ = {}  # so the API sends back full list without pagination

        filters = kwargs.get("filters")
        if filters:
            json_["filter"] = filters
            return json_

        return None
