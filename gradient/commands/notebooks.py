import abc

import halo
import six
from gradient import api_sdk
from gradient.commands.common import BaseCommand, ListCommandMixin, DetailsCommandMixin


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
        self.logger.log(self.get_instance_url(notebook_id))

    def get_instance_url(self, notebook_id):
        notebook = self.client.get(notebook_id)
        return notebook.url


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


class ShowNotebookDetailsCommand(DetailsCommandMixin, BaseNotebookCommand):
    def _get_table_data(self, instance):
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
