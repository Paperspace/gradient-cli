import abc
import pydoc

import halo
import six
import terminaltables

from gradient import api_sdk, exceptions
from gradient.commands.common import BaseCommand, ListCommandMixin
from gradient.commands.experiments import BaseCreateExperimentCommandMixin
from gradient.utils import get_terminal_lines


@six.add_metaclass(abc.ABCMeta)
class BaseHyperparameterCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.HyperparameterJobsClient(api_key=api_key, logger=logger)
        return client


class CreateHyperparameterCommand(BaseCreateExperimentCommandMixin, BaseHyperparameterCommand):
    SPINNER_MESSAGE = "Creating hyperparameter tuning job"
    CREATE_SUCCESS_MESSAGE_TEMPLATE = "Hyperparameter tuning job created with ID: {}"

    def _create(self, hyperparameter, use_vpc=False):
        handle = self.client.create(**hyperparameter)
        return handle


class CreateAndStartHyperparameterCommand(BaseCreateExperimentCommandMixin, BaseHyperparameterCommand):
    SPINNER_MESSAGE = "Creating and starting hyperparameter tuning job"
    CREATE_SUCCESS_MESSAGE_TEMPLATE = "Hyperparameter tuning job created and started with ID: {}"

    def _create(self, hyperparameter, use_vpc=False):
        handle = self.client.run(**hyperparameter)
        return handle


class ListHyperparametersCommand(ListCommandMixin, BaseHyperparameterCommand):
    def _get_instances(self, kwargs):
        try:
            instances = self.client.list()
        except api_sdk.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instances

    def _get_table_data(self, objects):
        data = [("Name", "ID", "Project ID")]
        for obj in objects:
            data.append((obj.name, obj.id, obj.project_id))
        return data


class HyperparameterDetailsCommand(BaseHyperparameterCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, id_):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instance = self._get_instance(id_)

        self._log_object(instance)

    def _get_instance(self, id_):
        """
        :rtype: api_sdk.Hyperparameter
        """
        try:
            instance = self.client.get(id_)
        except api_sdk.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instance

    @staticmethod
    def _make_table(obj):
        """
        :param api_sdk.Hyperparameter obj:
        """
        data = (
            ("ID", obj.id),
            ("Name", obj.name),
            ("Ports", obj.ports),
            ("Project ID", obj.project_id),
            ("Tuning command", obj.tuning_command),
            ("Worker command", obj.worker_command),
            ("Worker container", obj.worker_container),
            ("Worker count", obj.worker_count),
            ("Worker machine type", obj.worker_machine_type),
            ("Worker use dockerfile", obj.use_dockerfile or False),
            ("Workspace URL", obj.workspace_url),
        )
        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string

    def _log_object(self, instance):

        table_str = self._make_table(instance)
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)


class HyperparameterStartCommand(BaseHyperparameterCommand):
    def execute(self, id_):
        self.client.start(id_)
        self.logger.log("Hyperparameter tuning started")
