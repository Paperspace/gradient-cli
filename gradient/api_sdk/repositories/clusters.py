from gradient.api_sdk.config import config
from gradient.api_sdk.repositories.common import GetResource
from gradient.api_sdk.serializers.cluster import ClusterSchema


class ValidateClusterRepository(GetResource):
    SERIALIZER_CLS = ClusterSchema

    def get_request_url(self, **kwargs):
        return "/clusters/getCluster"

    def _get_api_url(self, use_vpc=False):
        return config.CONFIG_HOST

    def _get_request_params(self, kwargs):
        return {
            "id": kwargs.get("cluster_id")
        }
