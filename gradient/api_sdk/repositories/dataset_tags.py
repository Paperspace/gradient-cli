from .common import AlterResource, DeleteResource, GetResource, ListResources
from .datasets import DatasetMixin
from .. import serializers


class DatasetTagMixin(DatasetMixin):
    SERIALIZER_CLS = serializers.DatasetTagSchema

    @classmethod
    def get_request_url(cls, id='', name=None, **kwargs):
        dataset_id, _, ref = id.partition(':')
        if not name and ref:
            name = ref

        url = super(DatasetTagMixin, cls).get_request_url(id=dataset_id, **kwargs) + "/tags"
        if name:
            url += "/{}".format(name)
        return url


class ListDatasetTags(DatasetTagMixin, ListResources):
    def _get_request_params(self, kwargs):
        limit = kwargs.get("limit") or 20
        offset = kwargs.get("offset") or 0
        return {
            "filter[limit]": limit,
            "filter[skip]": offset,
            "filter[order][]": "name ASC",
        }


class SetDatasetTag(DatasetTagMixin, AlterResource):
    HANDLE_FIELD = "tag"

    def _get_request_json(self, instance):
        _, _, version = instance['id'].partition(':')
        instance = dict(instance)
        instance.pop('id', None)
        instance.pop('name', None)
        instance['version'] = version
        return instance

    def _send_request(self, client, url, json_data=None):
        response = client.put(url, json=json_data)
        return response


class GetDatasetTag(DatasetTagMixin, GetResource):
    pass


class DeleteDatasetTag(DatasetTagMixin, DeleteResource):
    pass
