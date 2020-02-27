import abc

import six
from halo import halo

from gradient import clilogger as gradient_logger, exceptions
from gradient.api_sdk import sdk_exceptions
from gradient.commands.common import ListCommandMixin


@six.add_metaclass(abc.ABCMeta)
class _ClustersCommand(object):
    def __init__(self, cluster_client, logger_=gradient_logger.CliLogger()):
        self.client = cluster_client
        self.logger = logger_

    @abc.abstractmethod
    def execute(self, **kwargs):
        pass


class ListClustersCommand(ListCommandMixin, _ClustersCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, **kwargs):
        return self._generate_data_table(**kwargs)

    def _get_instances(self, **kwargs):
        try:
            instances= self.client.list(**kwargs)
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


