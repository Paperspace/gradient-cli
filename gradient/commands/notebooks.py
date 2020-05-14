import abc
import json
import pydoc

import halo
import six
import terminaltables
from click import style

from gradient import api_sdk, exceptions
from gradient.api_sdk import sdk_exceptions
from gradient.cli_constants import CLI_PS_CLIENT_NAME
from gradient.cliutils import get_terminal_lines
from gradient.commands.common import BaseCommand, ListCommandMixin, DetailsCommandMixin, StreamMetricsCommand


@six.add_metaclass(abc.ABCMeta)
class BaseNotebookCommand(BaseCommand):
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


class StopNotebookCommand(BaseNotebookCommand):
    SPINNER_MESSAGE = "Stopping notebook"

    def execute(self, id):
        with halo.Halo(text=self.SPINNER_MESSAGE, spinner="dots"):
            self.client.stop(id)

        self.logger.log("Stopping notebook with id: {}".format(id))


class StartNotebookCommand(BaseNotebookCommand):
    SPINNER_MESSAGE = "Starting notebook"

    def execute(self, **kwargs):
        with halo.Halo(text=self.SPINNER_MESSAGE, spinner="dots"):
            notebook_id = self.client.start(**kwargs)

        self.logger.log("Started notebook with id: {}".format(notebook_id))
        self.logger.log(self.get_instance_url(notebook_id))

    def get_instance_url(self, notebook_id):
        notebook = self.client.get(notebook_id)
        return notebook.url


class ForkNotebookCommand(BaseNotebookCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Forking notebook"

    def execute(self, id_):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            handle = self.client.fork(id_)

        self.logger.log("Notebook forked to id: {}".format(handle))


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
        self.client.add_tags(notebook_id, **kwargs)
        self.logger.log("Tags added to notebook")


class NotebookRemoveTagsCommand(BaseNotebookCommand):
    def execute(self, notebook_id, *args, **kwargs):
        self.client.remove_tags(notebook_id, **kwargs)
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


class NotebookLogsCommand(BaseNotebookCommand):

    def execute(self, notebook_id, line, limit, follow):
        if follow:
            self.logger.log("Awaiting logs...")
            self._log_logs_continuously(notebook_id, line, limit)
        else:
            self._log_table_of_logs(notebook_id, line, limit)

    def _log_table_of_logs(self, notebook_id, line, limit):
        logs = self.client.logs(notebook_id, line, limit)
        if not logs:
            self.logger.log("No logs found")
            return

        table_str = self._make_table(logs, notebook_id)
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

    def _log_logs_continuously(self, notebook_id, line, limit):
        logs_gen = self.client.yield_logs(notebook_id, line, limit)
        for log in logs_gen:
            log_msg = "{}\t{}".format(*self._format_row(log))
            self.logger.log(log_msg)

    @staticmethod
    def _format_row(log_row):
        return (style(fg="red", text=str(log_row.line)),
                log_row.message)

    def _make_table(self, logs, notebook_id):
        table_title = "Notebook %s logs" % notebook_id
        table_data = [("LINE", "MESSAGE")]
        table = terminaltables.AsciiTable(table_data, title=table_title)

        for log in logs:
            table_data.append(self._format_row(log))

        return table.table


class ArtifactsListCommand(BaseNotebookCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, **kwargs):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            try:
                instances = self.client.artifacts_list(**kwargs)
            except sdk_exceptions.GradientSdkError as e:
                raise exceptions.ReceivingDataFailedError(e)

        self._log_objects_list(instances, kwargs)

    def _get_table_data(self, artifacts, kwargs):
        columns = ['Files']

        show_size = "size" in kwargs
        show_url = "url" in kwargs

        if show_size:
            columns.append('Size (in bytes)')
        if show_url:
            columns.append('URL')

        data = [tuple(columns)]
        for artifact in artifacts:
            row = [artifact.file]
            if show_size:
                row.append(artifact.size)
            if show_url:
                row.append(artifact.url)
            data.append(tuple(row))
        return data

    def _log_objects_list(self, objects, kwargs):
        if not objects:
            self.logger.warning("No data found")
            return

        table_data = self._get_table_data(objects, kwargs)
        table_str = self._make_table(table_data)
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

    @staticmethod
    def _make_table(table_data):
        ascii_table = terminaltables.AsciiTable(table_data)
        table_string = ascii_table.table
        return table_string
