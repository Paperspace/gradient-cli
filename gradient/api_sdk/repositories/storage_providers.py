from .common import AlterResource, CreateResource, DeleteResource, GetResource, ListResources
from .. import config, serializers


class StorageProviderMixin(object):
    SERIALIZER_CLS = serializers.StorageProviderSchema

    @staticmethod
    def _get_api_url(**kwargs):
        return config.config.CONFIG_HOST

    @staticmethod
    def get_request_url(**kwargs):
        url = "/storageProviders"
        if kwargs.get("id"):
            url += "/{}".format(kwargs["id"])
        return url


class ListStorageProviders(StorageProviderMixin, ListResources):
    def _get_request_params(self, kwargs):
        limit = kwargs.get("limit") or 20
        offset = kwargs.get("offset") or 0
        return {
            "filter[limit]": limit,
            "filter[skip]": offset,
            "filter[order][]": "name ASC",
        }


class CreateStorageProvider(StorageProviderMixin, CreateResource):
    HANDLE_FIELD = "id"


class GetStorageProvider(StorageProviderMixin, GetResource):
    pass


class UpdateStorageProvider(StorageProviderMixin, AlterResource):
    def _get_request_json(self, kwargs):
        data = dict(kwargs)
        if "id" in data:
            del data["id"]
        return data


class DeleteStorageProvider(StorageProviderMixin, DeleteResource):
    pass
