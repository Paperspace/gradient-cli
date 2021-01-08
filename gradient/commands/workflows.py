import abc
import json

import six

from halo import halo
from gradient import api_sdk
from gradient.cli_constants import CLI_PS_CLIENT_NAME
from gradient.commands.common import BaseCommand, ListCommandMixin, DetailsCommandMixin


@six.add_metaclass(abc.ABCMeta)
class DetailJSONCommandMixin(DetailsCommandMixin):
    def _get_table_data(self, instance):
        json_formatted_str = json.dumps(instance, indent=4)
        return json_formatted_str

    def _log_object(self, instance):
        if instance is None:
            self.logger.warning("Not found")
            return
        
        json_formatted_str = json.dumps(instance, indent=4)
        print(json_formatted_str)


@six.add_metaclass(abc.ABCMeta)
class BaseWorkflowCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.WorkflowsClient(
            api_key=api_key,
            logger=logger,
            ps_client_name=CLI_PS_CLIENT_NAME,
        )
        return client

class ListWorkflowsCommand(ListCommandMixin, BaseWorkflowCommand):
    def _get_instances(self, kwargs):
        instances = self.client.list(**kwargs)
        return instances

    def _get_table_data(self, objects):
        data = [('Name', 'ID')]
        for workflow in objects:
            data.append((
                workflow.name,
                workflow.id,
            ))
        return data

class ListWorkflowRunsCommand(ListCommandMixin, BaseWorkflowCommand):
    def _get_instances(self, kwargs):
        instances = self.client.list_runs(**kwargs)
        return instances
        
    def _get_table_data(self, objects):
        data = [('Run', 'Cluster ID', 'Status')]
        for workflow_run in objects:
            data.append((
                workflow_run['id'],
                workflow_run['cluster']['id'],
                workflow_run['status']['phase'],
            ))
        return data


class GetWorkflowCommand(DetailJSONCommandMixin, BaseWorkflowCommand):
    def execute(self, workflow_id):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instance = self.get_instance(workflow_id=workflow_id)

        self._log_object(instance)

    def get_instance(self, workflow_id):
        instance = self.client.get(workflow_id=workflow_id)
        if not hasattr(instance, 'spec'):
            instance['spec'] = "None"

        return instance

class GetWorkflowRunCommand(DetailJSONCommandMixin, BaseWorkflowCommand):
    def execute(self, workflow_id, run):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instance = self.get_instance(workflow_id=workflow_id, run=run)

        self._log_object(instance)

    def get_instance(self, workflow_id, run):
        instances = self.client.get_run(workflow_id=workflow_id, run=run)
        return instances



