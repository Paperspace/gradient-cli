import abc
import collections
import json
import pydoc

import six
import terminaltables
from click import style
from halo import halo

from gradient import api_sdk, exceptions
from gradient.api_sdk import sdk_exceptions
from gradient.api_sdk.config import config
from gradient.clilogger import CliLogger
from gradient.cliutils import get_terminal_lines, TerminalPrinter
from gradient.cli_constants import CLI_PS_CLIENT_NAME
from gradient.exceptions import ApplicationError


@six.add_metaclass(abc.ABCMeta)
class BaseCommand:
    def __init__(self, api_key, logger=CliLogger()):
        self.api_key = api_key
        self.client = self._get_client(api_key, logger)
        self.logger = logger

    def get_namespace(self):
        client = api_sdk.clients.http_client.API(
            config.CONFIG_HOST,
            api_key=self.api_key,
            logger=self.logger,
            ps_client_name=CLI_PS_CLIENT_NAME,
        )

        try:
            resp = client.get(url='/teams/namespace')
        except sdk_exceptions.GradientSdkError as e:
                raise exceptions.ReceivingDataFailedError(e)
        if isinstance(resp.json(), str):
            return resp.json()
        return ''

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def _get_client(self, api_key, logger):
        pass


@six.add_metaclass(abc.ABCMeta)
class ListCommandMixin(object):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."
    TOTAL_ITEMS_KEY = "total"

    def execute(self, **kwargs):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instances = self._get_instances(kwargs)

        self._log_objects_list(instances)

    @abc.abstractmethod
    def _get_instances(self, kwargs):
        pass

    @abc.abstractmethod
    def _get_table_data(self, objects):
        pass

    def _log_objects_list(self, objects):
        if not objects:
            self.logger.warning("No data found")
            return

        table_data = self._get_table_data(objects)
        table_str = self._make_list_table(table_data)
        self._print_table_to_terminal(table_str)

    def _print_table_to_terminal(self, table_str):
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

    @staticmethod
    def _make_list_table(table_data):
        ascii_table = terminaltables.AsciiTable(table_data)
        table_string = ascii_table.table
        return table_string

    def _generate_data_table(self, **kwargs):
        limit = kwargs.get("limit")
        offset = kwargs.get("offset")
        meta_data = dict()
        while self.TOTAL_ITEMS_KEY not in meta_data or offset < meta_data.get(self.TOTAL_ITEMS_KEY):
            with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
                kwargs["offset"] = offset
                instances, meta_data = self._get_instances(
                    **kwargs
                )
            next_iteration = False
            if instances:
                table_data = self._get_table_data(instances)
                table_str = self._make_list_table(table_data) + "\n"
                if offset + limit < meta_data.get(self.TOTAL_ITEMS_KEY):
                    next_iteration = True
            else:
                table_str = "No data found"

            yield table_str, next_iteration
            offset += limit


@six.add_metaclass(abc.ABCMeta)
class ListCommandPagerMixin(ListCommandMixin):
    def _get_instances(self, kwargs):
        limit = kwargs.get('limit') or 20
        offset = 0

        while True:
            with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
                results = self.client.list(limit=limit + 1, offset=offset, **kwargs)
            has_more = len(results) > limit
            yield results[:limit], has_more
            if not has_more:
                break
            offset += limit

    def execute(self, **kwargs):
        for instances, has_more in self._get_instances(kwargs):
            self._log_objects_list(instances)
            yield has_more


@six.add_metaclass(abc.ABCMeta)
class DetailsCommandMixin(object):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, id_):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instance = self._get_instance(id_)

        self._log_object(instance)

    def _get_instance(self, id_):
        instance = self.client.get(id_)

        return instance

    def _log_object(self, instance):
        if instance is None:
            self.logger.warning("Not found")
            return

        table_str = self._make_table(instance)
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

    def _make_table(self, instance):
        data = self._get_table_data(instance)
        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string

    @abc.abstractmethod
    def _get_table_data(self, instance):
        pass


class StreamMetricsCommand(ListCommandMixin):
    def __init__(self, *args, **kwargs):
        super(StreamMetricsCommand, self).__init__(*args, **kwargs)
        # {"metricName": {"pod_id": "value"}}
        self._recent_values = collections.OrderedDict()
        self.terminal_printer = None

    def execute(self, *args, **kwargs):
        self.terminal_printer = TerminalPrinter()
        self.terminal_printer.init()
        try:
            rv = super(StreamMetricsCommand, self).execute(*args, **kwargs)
        finally:
            self.terminal_printer.clear()
            self.terminal_printer.cleanup()

        return rv

    def _get_instances(self, kwargs):
        metrics_stream = self.client.stream_metrics(**kwargs)
        self._prepare_recent_values(kwargs["built_in_metrics"])
        return metrics_stream

    def _prepare_recent_values(self, builtin_metrics_names):
        for name in builtin_metrics_names:
            self._recent_values[name] = collections.OrderedDict()

    def _log_objects_list(self, metrics_stream):
        for raw_metric_date_response in metrics_stream:
            metric_data = json.loads(raw_metric_date_response)
            self._update_recent_values(metric_data)
            super(StreamMetricsCommand, self)._log_objects_list(raw_metric_date_response)

    def _update_recent_values(self, metric_data):
        metric_name = metric_data["chart_name"]
        metrics = metric_data["pod_metrics"]
        for pod_name, data in metrics.items():
            self._recent_values[metric_name][pod_name] = data["value"]

    def _print_table_to_terminal(self, table_str):
        self.terminal_printer.rewrite_screen(table_str)

    def _get_table_data(self, objects):
        metrics = list(self._recent_values.keys())
        table_ = ["Pod"] + metrics
        table_data = [table_]
        values = collections.OrderedDict()  # {pod_name: {metricName: value}}
        for metric_name, data in self._recent_values.items():
            for pod_name, value in data.items():
                pod_metrics = values.setdefault(pod_name, collections.OrderedDict())
                pod_metrics[metric_name] = value

        for pod_name, pod_metrics in sorted(values.items()):
            row = [pod_name]
            for metric_name in metrics:
                value = pod_metrics.get(metric_name, "")
                row.append(value)

            table_data.append(row)

        return table_data


class LogsCommandMixin(object):
    def execute(self, id, line, limit, follow):
        if follow:
            self.logger.log("Awaiting logs...")
            self._log_logs_continuously(id, line, limit)
        else:
            self._log_table_of_logs(id, line, limit)

    def _log_table_of_logs(self, id, line, limit):
        logs = self.client.logs(id, line, limit)
        if not logs:
            raise ApplicationError("No logs found")

        table_str = self._make_table(logs, id)
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

    def _log_logs_continuously(self, id, line, limit):
        logs_gen = self._get_logs_generator(id, line, limit)
        for log in logs_gen:
            log_msg = self._get_log_row_string(id, log)
            self.logger.log(log_msg)

    def _get_logs_generator(self, id, line, limit):
        logs_gen = self.client.yield_logs(id, line, limit)
        return logs_gen

    def _make_table(self, logs, id):
        table_title = "%s %s logs" % (self.ENTITY, id)
        table_data = [("LINE", "MESSAGE")]
        table = terminaltables.AsciiTable(table_data, title=table_title)

        for log in logs:
            table_data.append(self._format_row(log))

        return table.table

    def _get_log_row_string(self, id, log):
        log_msg = "{}\t{}".format(*self._format_row(log))
        return log_msg

    @staticmethod
    def _format_row(log_row):
        return (style(fg="red", text=str(log_row.line)),
                log_row.message)
