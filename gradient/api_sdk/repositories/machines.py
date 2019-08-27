from gradient.config import config
from .common import BaseRepository, CreateResource
from .. import serializers


class MachinesApiUrlMixin(object):
    def _get_api_url(self, use_vpc=False):
        return config.CONFIG_HOST


class CheckMachineAvailability(MachinesApiUrlMixin, BaseRepository):
    def get_request_url(self, **kwargs):
        return "/machines/getAvailability/"

    def get(self, machine_type, region):
        kwargs = {"machineType": machine_type,
                  "region": region}
        response = self._get(kwargs)
        self._validate_response(response)
        is_available = response.data["available"]
        return is_available

    def _get_request_params(self, kwargs):
        return kwargs


class CreateMachine(MachinesApiUrlMixin, CreateResource):
    SERIALIZER_CLS = serializers.MachineSchema
    HANDLE_FIELD = "id"

    def get_request_url(self, **kwargs):
        return "/machines/createSingleMachinePublic/"
