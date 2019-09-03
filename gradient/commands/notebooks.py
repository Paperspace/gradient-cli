import abc
import pydoc

import halo
import six
import terminaltables

from gradient import api_sdk
from gradient.commands.common import BaseCommand, ListCommandMixin
from gradient.utils import get_terminal_lines


@six.add_metaclass(abc.ABCMeta)
class BaseNotebookCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.NotebooksClient(api_key=api_key, logger=logger)
        return client


class CreateNotebookCommand(BaseNotebookCommand):
    SPINNER_MESSAGE = "Creating new notebook"

    def execute(self, **kwargs):
        with halo.Halo(text=self.SPINNER_MESSAGE, spinner="dots"):
            notebook_id = self.client.create(**kwargs)

        self.logger.log("Created new notebook with id: {}".format(notebook_id))


class DeleteNotebookCommand(BaseNotebookCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Deleting notebook"

    def execute(self, id_):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            self.client.delete(id_)

        self.logger.log("Notebook deleted")


class ListNotebooksCommand(ListCommandMixin, BaseNotebookCommand):
    SPINNER_MESSAGE = "Waiting for data"

    def _get_instances(self, kwargs):
        notebooks = self.client.list()
        return notebooks

    def _get_table_data(self, notebooks):
        data = [("Name", "ID")]
        for obj in notebooks:
            data.append((obj.name, obj.id))
        return data


class ShowNotebookDetailsCommand(BaseNotebookCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data"

    def execute(self, id_):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instance = self._get_instance(id_)

        self._log_object(instance)

    def _get_instance(self, id_):
        """
        :rtype: api_sdk.Notebook
        """
        instance = self.client.get(id_)
        return instance

    def _log_object(self, instance):

        table_str = self._make_table(instance)
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

    def _make_table(self, instance):
        """
        :param api_sdk.Notebook:
        """
        data = self._get_table_data(instance)
        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string

    @staticmethod
    def _get_table_data(instance):
        """
        :param api_sdk.Notebook instance:
        """
        data = (
            ("Name", instance.name),
            ("ID", instance.id),
            ("VM Type", instance.vm_type),
            ("State", instance.state),
            ("FQDN", instance.fqdn),
        )
        return data
