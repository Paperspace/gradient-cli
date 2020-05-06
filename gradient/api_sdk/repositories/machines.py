import time

from .common import BaseRepository, CreateResource, DeleteResource, ListResources, StartResource, StopResource, \
    GetResource, AlterResource
from .. import serializers, models
from ..config import config
from ..serializers import MachineSchema


class MachinesApiUrlMixin(object):
    def _get_api_url(self, **kwargs):
        return config.CONFIG_HOST


class CheckMachineAvailability(MachinesApiUrlMixin, BaseRepository):
    def get_request_url(self, **kwargs):
        return "/machines/getAvailability/"

    def get(self, machine_type, region):
        kwargs = {"machineType": machine_type,
                  "region": region}
        response = self._get(**kwargs)
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


class DeleteMachine(MachinesApiUrlMixin, DeleteResource):
    def get_request_url(self, **kwargs):
        machine_id = kwargs["id"]
        url = "/machines/{}/destroyMachine/".format(machine_id)
        return url

    def _send_request(self, client, url, json_data=None):
        response = client.post(url, json=json_data)
        return response

    def _get_request_json(self, kwargs):
        release_public_ip = kwargs["release_public_ip"]
        json_ = {"releasePublicIp": release_public_ip} if release_public_ip else None
        return json_


class ListMachines(MachinesApiUrlMixin, ListResources):
    def _parse_objects(self, data, **kwargs):
        instances = []

        for machine_dict in data:
            machine = serializers.MachineSchema().get_instance(machine_dict)
            instances.append(machine)

        return instances

    def get_request_url(self, **kwargs):
        return "/machines/getMachines/"

    def _get_request_json(self, kwargs):
        instance = models.Machine(**kwargs)
        serializer = serializers.MachineSchemaForListing()
        marshaled = serializer.dump(instance)
        instance_dict = marshaled.data
        instance_dict_without_nulls = {key: val for key, val in instance_dict.items() if val is not None}
        json_ = {"params": instance_dict_without_nulls} if instance_dict_without_nulls else None
        return json_


class RestartMachine(MachinesApiUrlMixin, StartResource):
    VALIDATION_ERROR_MESSAGE = "Unable to restart instance"

    def restart(self, id_, **kwargs):
        self._run(id=id_, **kwargs)

    def get_request_url(self, **kwargs):
        machine_id = kwargs["id"]
        url = "/machines/{}/restart/".format(machine_id)
        return url

    def _send_request(self, client, url, json_data=None):
        response = client.post(url, json=json_data)
        return response


class StartMachine(MachinesApiUrlMixin, StartResource):
    def restart(self, id_, **kwargs):
        self._run(id=id_, **kwargs)

    def get_request_url(self, **kwargs):
        machine_id = kwargs["id"]
        url = "/machines/{}/start/".format(machine_id)
        return url

    def _send_request(self, client, url, json_data=None):
        response = client.post(url, json=json_data)
        return response


class StopMachine(MachinesApiUrlMixin, StopResource):
    def restart(self, id_):
        self._run(id=id_)

    def get_request_url(self, **kwargs):
        machine_id = kwargs["id"]
        url = "/machines/{}/stop/".format(machine_id)
        return url

    def _send_request(self, client, url, json_data=None):
        response = client.post(url, json=json_data)
        return response


class GetMachine(MachinesApiUrlMixin, GetResource):
    SERIALIZER_CLS = MachineSchema

    def get_request_url(self, **kwargs):
        return "/machines/getMachinePublic/"

    def _get_request_params(self, kwargs):
        machine_id = kwargs["id"]
        params = {"machineId": machine_id}
        return params


class UpdateMachine(MachinesApiUrlMixin, AlterResource):
    SERIALIZER_CLS = serializers.MachineSchema
    VALIDATION_ERROR_MESSAGE = "Failed to update resource"

    def get_request_url(self, **kwargs):
        machine_id = kwargs["id"]
        url = "/machines/{}/updateMachinePublic/".format(machine_id)
        return url

    def _get_request_json(self, kwargs):
        kwargs.pop("id", None)
        return kwargs


class GetMachineUtilization(MachinesApiUrlMixin, GetResource):
    def _parse_object(self, data, **kwargs):
        instance = models.MachineUtilization(
            machine_id=data["machineId"],
            machine_seconds_used=data["utilization"].get("secondsUsed") if "utilization" in data else None,
            machine_billing_month=data["utilization"].get("billingMonth") if "utilization" in data else None,
            machine_hourly_rate=data["utilization"].get("hourlyRate") if "utilization" in data else None,
            storage_seconds_used=data["storageUtilization"].get("secondsUsed") if "utilization" in data else None,
            storage_billing_month=data["storageUtilization"].get("billingMonth") if "utilization" in data else None,
            storage_monthly_rate=data["storageUtilization"].get("monthlyRate") if "utilization" in data else None,
        )
        return instance

    def get_request_url(self, **kwargs):
        return "machines/getUtilization/"

    def _get_request_params(self, kwargs):
        d = {
            "machineId": kwargs["id"],
            "billingMonth": kwargs["billing_month"]
        }
        return d


class WaitForState(object):
    def __init__(self, api_key, logger, ps_client_name=None):
        self.api_key = api_key
        self.logger = logger
        self.get_machine_repository = GetMachine(api_key=api_key, logger=logger, ps_client_name=ps_client_name)

    def wait_for_state(self, machine_id, state, interval=5):

        while True:
            current_state = self._get_machine_state(machine_id)
            if current_state == state:
                return

            time.sleep(interval)

    def _get_machine_state(self, machine_id):
        machine = self.get_machine_repository.get(id=machine_id)
        return machine.state
