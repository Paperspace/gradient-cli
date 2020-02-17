import abc

import six

from gradient import version, logger as gradient_logger, exceptions
from gradient.commands.common import ListCommandMixin


@six.add_metaclass(abc.ABCMeta)
class _ClustersCommand(object):
    def __init__(self, cluster_client, logger_=gradient_logger.Logger()):
        self.client = cluster_client
        self.logger = logger_

    @abc.abstractmethod
    def execute(self, **kwargs):
        pass


class ListClustersCommand(ListCommandMixin, _ClustersCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, **kwargs):
        return self._generate_data_table(**kwargs)
