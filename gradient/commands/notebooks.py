import abc

import halo
import six

from gradient import api_sdk
from gradient.commands.common import BaseCommand


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
