from gradient.config import config
from . import common
from .. import serializers, models


class GetTensorboardApiUrlMixin(object):
    def _get_api_url(self, use_vpc=False):
        return config.CONFIG_HOST


class ParseTensorboardMixin(object):
    def _parse_object(self, instance_dict, **kwargs):
        # this ugly hack is here because marshmallow disallows reading value into `id` field
        # if JSON's field was named differently (despite using load_from in schema definition)
        instance_dict["id"] = instance_dict["handle"]

        machine_instance_dict = instance_dict.get("instance")
        if machine_instance_dict:
            machine_instance = serializers.InstanceSchema().get_instance(machine_instance_dict)
        else:
            machine_instance = models.Instance()

        instance = super(ParseTensorboardMixin, self)._parse_object(instance_dict)
        instance.instance = machine_instance
        return instance


class CreateTensorboard(GetTensorboardApiUrlMixin, common.CreateResource):
    SERIALIZER_CLS = serializers.TensorboardSchema

    def get_request_url(self, **kwargs):
        return "/tensorboards/v1/"

    def _get_id_from_response(self, response):
        handle = response.data["data"]["handle"]
        return handle


class GetTensorboard(ParseTensorboardMixin, GetTensorboardApiUrlMixin, common.GetResource):
    SERIALIZER_CLS = serializers.TensorboardSchema

    def get_request_url(self, **kwargs):
        id_ = kwargs["id"]
        return "/tensorboards/v1/{}/".format(id_)

    def _parse_object(self, instance_dict, **kwargs):
        instance_dict = instance_dict["data"]
        instance = super(GetTensorboard, self)._parse_object(instance_dict)
        return instance


class ListTensorboards(ParseTensorboardMixin, GetTensorboardApiUrlMixin, common.ListResources):
    SERIALIZER_CLS = serializers.TensorboardSchema

    def _get_instance_dicts(self, data, **kwargs):
        instance_dicts = data["data"]
        return instance_dicts

    def get_request_url(self, **kwargs):
        return "/tensorboards/v1/"
