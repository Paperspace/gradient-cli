import abc

import six

from gradient import api_sdk
from gradient.cli_constants import CLI_PS_CLIENT_NAME
from gradient.commands.common import BaseCommand, ListCommandMixin


@six.add_metaclass(abc.ABCMeta)
class BaseMachineTypesCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.MachineTypesClient(
            api_key=api_key,
            logger=logger,
            ps_client_name=CLI_PS_CLIENT_NAME,
        )
        return client


class ListMachineTypesCommand(ListCommandMixin, BaseMachineTypesCommand):
    def _get_instances(self, kwargs):
        instances = self.client.list(**kwargs)
        return instances

    def _get_table_data(self, objects):
        """
        :param list[VmTypeSchema] objects: object
        """
        data = [("Name", "Kind", "CPU Count", "RAM [Bytes]", "GPU Count", "GPU Model", "Clusters")]
        for obj in objects:
            name = obj.label
            kind = obj.kind
            cpu_count = obj.cpu_count
            ram_in_bytes = obj.ram_in_bytes
            gpu_count = obj.gpu_count
            gpu_model = obj.gpu_model.label if obj.gpu_model else "N/A"
            clusters = ", ".join(obj.clusters) if obj.clusters else ""

            data.append((name, kind, cpu_count, ram_in_bytes, gpu_count, gpu_model, clusters))

        return data
