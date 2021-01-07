import abc

import six

from gradient import api_sdk
from gradient.cli_constants import CLI_PS_CLIENT_NAME
from gradient.commands.common import BaseCommand, ListCommandMixin


@six.add_metaclass(abc.ABCMeta)
class BaseWorkflowCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.WorkflowClient(
            api_key=api_key,
            logger=logger,
            ps_client_name=CLI_PS_CLIENT_NAME,
        )
        return client

class ListWorkflowsCommand(ListCommandMixin, BaseWorkflowCommand):
    def _get_instances(self, kwargs):
        instances = self.client.list(**kwargs)
        return instances

class ListWorkflowRunsCommand(ListCommandMixin, BaseWorkflowCommand):
    def _get_instances(self, kwargs):
        instances = self.client.list_runs(**kwargs)
        return instances
