import gradient.api_sdk.config
from gradient import config
from .. import serializers
from ..repositories.common import ListResources, DeleteResource


class ParseModelDictMixin(object):
    def _parse_object(self, model_dict, **kwargs):
        """
        :param dict model_dict:
        :rtype Model
        """
        model = serializers.Model().get_instance(model_dict)
        return model


class GetBaseModelsApiUrlMixin(object):
    def _get_api_url(self, **_):
        return gradient.api_sdk.config.config.CONFIG_HOST


class ListModels(GetBaseModelsApiUrlMixin, ParseModelDictMixin, ListResources):
    def get_request_url(self, **kwargs):
        return "/mlModels/getModelList/"

    def _parse_objects(self, data, **kwargs):
        experiments = []
        for model_dict in data["modelList"]:
            experiment = self._parse_object(model_dict)
            experiments.append(experiment)

        return experiments

    def _get_request_params(self, kwargs):
        return {"limit": -1}

    def _get_request_json(self, kwargs):
        filters = {}
        if kwargs.get("experiment_id"):
            filters["experimentId"] = kwargs.get("experiment_id")
        if kwargs.get("project_id"):
            filters["projectId"] = kwargs.get("project_id")

        if not filters:
            return None

        json_ = {"filter": {"where": {"and": [filters]}}}
        return json_


class DeleteModel(GetBaseModelsApiUrlMixin, DeleteResource):
    def get_request_url(self, **kwargs):
        return "/mlModels/deleteModel/"

    def _send_request(self, client, url, json_data=None):
        response = client.post(url, json=json_data)
        return response

    def _get_request_json(self, kwargs):
        return kwargs
