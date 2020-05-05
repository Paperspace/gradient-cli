from . import common
from .. import config
from .. import serializers, models


class GetTensorboardApiUrlMixin(object):
    def _get_api_url(self, **kwargs):
        return config.config.CONFIG_SERVICE_HOST


class ParseTensorboardMixin(object):
    def _parse_object(self, instance_dict, **kwargs):
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
        handle = response.data["data"]["id"]
        return handle


class GetTensorboard(ParseTensorboardMixin, GetTensorboardApiUrlMixin, common.GetResource):
    SERIALIZER_CLS = serializers.TensorboardDetailSchema

    def get_request_url(self, **kwargs):
        id_ = kwargs["id"]
        return "/tensorboards/v1/{}/".format(id_)

    def _parse_object(self, instance_dict, **kwargs):
        instance_dict = instance_dict["data"]
        instance = super(GetTensorboard, self)._parse_object(instance_dict)
        return instance


class ListTensorboards(ParseTensorboardMixin, GetTensorboardApiUrlMixin, common.ListResources):
    SERIALIZER_CLS = serializers.TensorboardDetailSchema

    def _get_instance_dicts(self, data, **kwargs):
        instance_dicts = data["data"]
        return instance_dicts

    def get_request_url(self, **kwargs):
        return "/tensorboards/v1/"


class UpdateTensorboard(ParseTensorboardMixin, GetTensorboardApiUrlMixin, common.AlterResource):
    VALIDATION_ERROR_MESSAGE = "Failed to update resource"

    def update(self, id, **kwargs):
        resp = self._run(id=id, **kwargs)
        tensorboard = self._parse_object(resp.data)
        return tensorboard

    def get_request_url(self, **kwargs):
        return "/tensorboards/v1/{}".format(kwargs["id"])

    def _send_request(self, client, url, json_data=None):
        response = client.put(url, json=json_data)
        return response

    def _get_request_json(self, kwargs):
        return {
            "added_experiments": kwargs.get("added_experiments", list()),
            "removed_experiments": kwargs.get("removed_experiments", list())
        }

    def _parse_object(self, instance_dict, **kwargs):
        instance_dict = instance_dict["data"]
        instance = self._get_instance(instance_dict)
        return instance

    def _get_instance(self, instance_dict):
        machine_instance_dict = instance_dict.get("instance")
        if machine_instance_dict:
            machine_instance = serializers.InstanceSchema().get_instance(machine_instance_dict)
        else:
            machine_instance = models.Instance()

        instance = serializers.TensorboardDetailSchema().get_instance(instance_dict)
        instance.instance = machine_instance
        return instance


class DeleteTensorboard(GetTensorboardApiUrlMixin, common.DeleteResource):
    VALIDATION_ERROR_MESSAGE = "Failed to delete resource"

    def get_request_url(self, **kwargs):
        return "/tensorboards/v1/{}".format(kwargs["id"])
