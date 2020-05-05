import json
from collections import OrderedDict

from ..config import config
from ..repositories.common import GetResource, ListResources
from ..sdk_exceptions import MalformedResponseError
from ..serializers.cluster import ClusterSchema


class ValidateClusterRepository(GetResource):
    SERIALIZER_CLS = ClusterSchema

    def get_request_url(self, **kwargs):
        return "/clusters/getCluster"

    def _get_api_url(self, **kwargs):
        return config.CONFIG_HOST

    def _get_request_params(self, kwargs):
        return {
            "id": kwargs.get("cluster_id")
        }

    def _parse_object(self, instance_dict, **kwargs):
        """
        :param dict instance_dict:
        :return: model instance
        """
        instance = self.SERIALIZER_CLS().dump(instance_dict)
        if instance.errors:
            raise MalformedResponseError(instance.errors)
        return instance.data


class ListClusters(ListResources):
    SERIALIZER_CLS = ClusterSchema

    def get_request_url(self, **kwargs):
        return "/clusters/getClusters"

    def _get_api_url(self, **kwargs):
        return config.CONFIG_HOST

    def _get_request_params(self, kwargs):
        filter = OrderedDict()
        filter["limit"] = kwargs.get("limit")
        filter["offset"] = kwargs.get("offset")
        filter["where"] = {
            "isPrivate": True
        }

        return {
            "filter": json.dumps(OrderedDict(filter))
        }
