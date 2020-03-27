import abc

import six
from halo import halo

from gradient import exceptions, api_sdk
from gradient.api_sdk import sdk_exceptions
from gradient.cli_constants import CLI_PS_CLIENT_NAME
from gradient.commands.common import ListCommandMixin, BaseCommand


@six.add_metaclass(abc.ABCMeta)
class ClustersCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.ClustersClient(
            api_key=api_key,
            logger=logger,
            ps_client_name=CLI_PS_CLIENT_NAME,
        )
        return client


class ListClustersCommand(ListCommandMixin, ClustersCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, **kwargs):
        return self._generate_data_table(**kwargs)

    def _get_instances(self, **kwargs):
        try:
            instances = self.client.list(**kwargs)
        except sdk_exceptions.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instances

    def _get_table_data(self, objects):
        data = [("ID", "Name", "Type")]

        for cluster in objects:
            handle = cluster.id
            name = cluster.name
            type = cluster.type
            data.append((handle, name, type))
        return data

    def _generate_data_table(self, **kwargs):
        limit = kwargs.get("limit")
        offset = kwargs.get("offset")
        next_iteration = True

        while next_iteration:
            with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
                kwargs["offset"] = offset
                instances = self._get_instances(
                    **kwargs
                )
            if instances:
                table_data = self._get_table_data(instances)
                table_str = self._make_list_table(table_data) + "\n"
            else:
                table_str = "No data found"

            if len(instances) < limit:
                next_iteration = False

            yield table_str, next_iteration
            offset += limit
