from .common import AlterResource, CreateResource, DeleteResource, GetResource, ListResources
from .. import config, serializers


class DatasetMixin(object):
    SERIALIZER_CLS = serializers.DatasetSchema

    @staticmethod
    def _get_api_url(**kwargs):
        return config.config.CONFIG_HOST

    @staticmethod
    def get_request_url(**kwargs):
        url = "/datasets"
        if kwargs.get("id"):
            url += "/{}".format(kwargs["id"])
        return url


class ListDatasets(DatasetMixin, ListResources):
    def _get_request_params(self, kwargs):
        limit = kwargs.get("limit") or 20
        offset = kwargs.get("offset") or 0
        return {
            "filter[limit]": limit,
            "filter[skip]": offset,
            "filter[order][]": "name ASC",
        }


class CreateDataset(DatasetMixin, CreateResource):
    HANDLE_FIELD = "id"


class GetDataset(DatasetMixin, GetResource):
    pass


class UpdateDataset(DatasetMixin, AlterResource):
    def _get_request_json(self, kwargs):
        data = dict(kwargs)
        if "id" in data:
            del data["id"]
        return data


class DeleteDataset(DatasetMixin, DeleteResource):
    pass


class GetDatasetRef(DatasetMixin, GetResource):
    SERIALIZER_CLS = serializers.DatasetRefSchema

    @staticmethod
    def get_request_url(**kwargs):
        return "/datasets/ref/{}".format(kwargs["id"])
