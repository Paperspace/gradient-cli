from .common import BaseRepository, AlterResource, CreateResource, DeleteResource, GetResource, ListResources
from .datasets import DatasetMixin
from .. import serializers


class DatasetVersionMixin(DatasetMixin):
    SERIALIZER_CLS = serializers.DatasetVersionSchema

    @classmethod
    def get_request_url(cls, id="", **kwargs):
        dataset_id, _, version = id.partition(":")

        url = super(DatasetVersionMixin, cls).get_request_url(id=dataset_id, **kwargs) + "/versions"
        if version:
            url += "/{}".format(version)
        return url


class ListDatasetVersions(DatasetVersionMixin, ListResources):
    def _get_request_params(self, kwargs):
        limit = kwargs.get("limit") or 20
        offset = kwargs.get("offset") or 0
        is_committed = bool(kwargs.get("is_committed", True))
        return {
            "filter[where][isCommitted]": str(is_committed).lower(),
            "filter[limit]": limit,
            "filter[skip]": offset,
            "filter[order][]": "dtCreated DESC",
        }


class CreateDatasetVersion(DatasetVersionMixin, CreateResource):
    HANDLE_FIELD = "version"

    def _get_request_json(self, instance_dict):
        instance_dict = dict(instance_dict)
        instance_dict.pop("id", None)
        return instance_dict


class GetDatasetVersion(DatasetVersionMixin, GetResource):
    pass


class UpdateDatasetVersion(DatasetVersionMixin, AlterResource):
    def _get_request_json(self, kwargs):
        data = dict(kwargs)
        if "id" in data:
            del data["id"]
        return data


class DeleteDatasetVersion(DatasetVersionMixin, DeleteResource):
    pass


class GenerateDatasetVersionPreSignedS3Urls(DatasetVersionMixin, BaseRepository):
    @classmethod
    def get_request_url(cls, id=None, **kwargs):
        return super(GenerateDatasetVersionPreSignedS3Urls, cls).get_request_url(id=id) + "/s3/preSignedUrls"

    def generate(self, id, calls):
        response = self._get(id=id, calls=calls)
        self._validate_response(response)
        return serializers.DatasetVersionPreSignedURLSchema().get_instance(response.data, many=True)

    def _get_request_json(self, kwargs):
        return {'calls': kwargs['calls']}

    def _send_request(self, client, url, json=None, params=None):
        return client.post(url, json=json, params=params)
