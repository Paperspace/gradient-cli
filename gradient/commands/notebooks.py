import abc
import json

import halo
import six

from gradient import api_sdk, exceptions
from gradient.api_sdk import sdk_exceptions
from gradient.cli_constants import CLI_PS_CLIENT_NAME
from gradient.commands.common import BaseCommand, ListCommandMixin, DetailsCommandMixin, StreamMetricsCommand


@six.add_metaclass(abc.ABCMeta)
class BaseNotebookCommand(BaseCommand):
    entity = "notebook"

    def _get_client(self, api_key, logger):
        client = api_sdk.clients.NotebooksClient(
            api_key=api_key,
            logger=logger,
            ps_client_name=CLI_PS_CLIENT_NAME,
        )
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

    def _get_instances(self, **kwargs):
        limit = kwargs.get("limit")
        offset = kwargs.get("offset")
        tags = kwargs.get("tags")
        get_meta = True
        try:
            instances, meta_data = self.client.list(get_meta=get_meta, limit=limit, offset=offset, tags=tags)
        except sdk_exceptions.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)
        return instances, meta_data

    def _get_table_data(self, notebooks):
        data = [("Name", "ID")]
        for obj in notebooks:
            data.append((obj.name, obj.id))
        return data

    def execute(self, **kwargs):
        return self._generate_data_table(**kwargs)


class ShowNotebookDetailsCommand(DetailsCommandMixin, BaseNotebookCommand):
    def _get_table_data(self, instance):
        """
        :param api_sdk.Notebook instance:
        """
        tags_string = ", ".join(instance.tags)

        data = (
            ("Name", instance.name),
            ("ID", instance.id),
            ("VM Type", instance.vm_type),
            ("State", instance.state),
            ("FQDN", instance.fqdn),
            ("Tags", tags_string),
        )
        return data


class NotebookAddTagsCommand(BaseNotebookCommand):
    def execute(self, notebook_id, *args, **kwargs):
        self.client.add_tags(notebook_id, entity=self.entity, **kwargs)
        self.logger.log("Tags added to notebook")


class NotebookRemoveTagsCommand(BaseNotebookCommand):
    def execute(self, notebook_id, *args, **kwargs):
        self.client.remove_tags(notebook_id, entity=self.entity, **kwargs)
        self.logger.log("Tags removed from notebook")


class GetNotebookMetricsCommand(BaseNotebookCommand):
    def execute(self, notebook_id, start, end, interval, built_in_metrics, *args, **kwargs):
        metrics = self.client.get_metrics(
            notebook_id,
            start=start,
            end=end,
            built_in_metrics=built_in_metrics,
            interval=interval,
        )
        formatted_metrics = json.dumps(metrics, indent=2, sort_keys=True)
        self.logger.log(formatted_metrics)


class StreamNotebookMetricsCommand(StreamMetricsCommand, BaseNotebookCommand):
    pass
