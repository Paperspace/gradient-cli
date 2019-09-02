from gradient import config
from .common import CreateResource
from .. import serializers


class GetNotebookApiUrlMixin(object):
    def _get_api_url(self, use_vpc=False):
        return config.config.CONFIG_HOST


class CreateNotebook(GetNotebookApiUrlMixin, CreateResource):
    SERIALIZER_CLS = serializers.NotebookSchema

    def get_request_url(self, **kwargs):
        return "notebooks/createNotebook"

    def _process_instance_dict(self, instance_dict):
        # the API requires this field but marshmallow does not create it if it's value is None
        instance_dict.setdefault("containerId")
        return instance_dict
