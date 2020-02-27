import glob
import os

import gradient.api_sdk.config
from .. import serializers
from ..repositories.common import ListResources, DeleteResource, CreateResource, GetResource
from ..sdk_exceptions import ResourceFetchingError


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

        if filters:
            json_ = {"filter": {"where": {"and": [filters]}}}
        else:
            json_ = {}

        tags = kwargs.get("tags")
        if tags:
            json_["tagFilter"] = tags

        return json_ or None


class DeleteModel(GetBaseModelsApiUrlMixin, DeleteResource):
    def get_request_url(self, **kwargs):
        return "/mlModels/deleteModel/"

    def _send_request(self, client, url, json_data=None):
        response = client.post(url, json=json_data)
        return response

    def _get_request_json(self, kwargs):
        return kwargs


class UploadModel(GetBaseModelsApiUrlMixin, CreateResource):
    SERIALIZER_CLS = serializers.Model
    HANDLE_FIELD = "id"

    def get_request_url(self, **kwargs):
        return "/mlModels/createModel"

    def _get_request_params(self, kwargs):
        return kwargs

    def _get_request_json(self, instance_dict):
        return None

    def _get_request_files(self, path):
        """
        :param str path: path to Model that will be uploaded
        """
        if not path:
            return None

        return self._prepare_files(path)

    @staticmethod
    def _prepare_files(path):
        files = list()
        if os.path.isfile(path):
            file_name = os.path.basename(path)
            files.append((file_name, open(path, "rb")))
        elif os.path.isdir(path):
            files_path = glob.glob(path + "/**", recursive=True)
            for file_path in files_path:
                if os.path.isfile(file_path):
                    file_name = os.path.relpath(file_path, path)
                    files.append((file_name, open(file_path, "rb")))
        return files


class GetModel(GetBaseModelsApiUrlMixin, GetResource):
    SERIALIZER_CLS = serializers.Model

    def get_request_url(self, **kwargs):
        return "/mlModels/getModelList/"

    def _get_request_json(self, kwargs):
        model_id = kwargs["model_id"]
        json_ = {"filter": {"where": {"and": [{"id": model_id}]}}}
        return json_

    def _parse_object(self, instance_dict, **kwargs):
        try:
            model_dict = instance_dict["modelList"][0]
        except (IndexError, TypeError):
            raise ResourceFetchingError("Model not found")

        instance = self.SERIALIZER_CLS().get_instance(model_dict)
        return instance


class ListModelFiles(GetBaseModelsApiUrlMixin, ListResources):
    SERIALIZER_CLS = serializers.ModelFileSchema

    def get_request_url(self, **kwargs):
        return "/mlModels/listFiles/"

    def _get_request_json(self, kwargs):
        json_ = {"id": kwargs["model_id"]}
        if kwargs.get("links"):
            json_["links"] = True
        if kwargs.get("size"):
            json_["size"] = True

        return json_
