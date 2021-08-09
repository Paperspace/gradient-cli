import abc
import json
import os

import six
import yaml

from halo import halo
from gradient import api_sdk
from gradient.cli_constants import CLI_PS_CLIENT_NAME
from gradient.exceptions import ApplicationError
from gradient.commands.common import BaseCommand, ListCommandMixin, DetailsCommandMixin, LogsCommandMixin


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


class CreateWorkflowCommand(BaseWorkflowCommand, DetailsCommandMixin):
    def _get_table_data(self, instance):
        data = [('Name', 'ID')]
        data.append((
            instance['name'],
            instance['id'],
        ))

        return data

    def execute(self, name, project_id):
        workflow = self.client.create(name, project_id)
        self._log_object(workflow)

        return workflow


class CreateWorkflowRunCommand(BaseWorkflowCommand):
    def execute(self, spec_path=None, input_path=None, workflow_id=None, cluster_id=None):
        spec = None
        inputs = None
        if spec_path:
            if not os.path.exists(spec_path):
                raise ApplicationError(
                    'Source path not found: {}'.format(spec_path))
            else:
                yaml_spec = open(spec_path, 'r')
                spec = yaml.safe_load(yaml_spec)

        if input_path:
            if not os.path.exists(input_path):
                raise ApplicationError(
                    'Source path not found: {}'.format(input_path))
            else:
                yaml_inputs = open(input_path, 'r')
                inputs = yaml.safe_load(yaml_inputs)

        workflow = self.client.run_workflow(
            spec=spec, inputs=inputs, workflow_id=workflow_id, cluster_id=cluster_id)

        logId = workflow.get('status', {}).get('logId')
        if logId is not None:
            self.logger.log("Created workflow run {}".format(logId))
        return workflow


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
        data = [('Run', 'Cluster ID', 'Status', 'Log ID')]
        for workflow_run in objects:
            data.append((
                workflow_run['id'],
                workflow_run['cluster']['id'],
                workflow_run['status']['phase'],
                workflow_run['status']['logId'],
            ))
        return data


class GetWorkflowCommand(DetailJSONCommandMixin, BaseWorkflowCommand):
    def execute(self, workflow_id):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instance = self.get_instance(workflow_id=workflow_id)

        self._log_object(instance)

    def get_instance(self, workflow_id):
        instance = self.client.get(workflow_id=workflow_id)
        return instance


class GetWorkflowRunCommand(DetailJSONCommandMixin, BaseWorkflowCommand):
    def execute(self, workflow_id, run):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instance = self.get_instance(workflow_id=workflow_id, run=run)

        self._log_object(instance)

    def get_instance(self, workflow_id, run):
        instance = self.client.get_run(workflow_id=workflow_id, run=run)
        return instance


class WorkflowLogsCommand(LogsCommandMixin, BaseWorkflowCommand):
    ENTITY = "Workflows"
