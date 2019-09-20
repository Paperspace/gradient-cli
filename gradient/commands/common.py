import abc
import pydoc

import six
import terminaltables
from halo import halo

from gradient.logger import Logger
from gradient.utils import get_terminal_lines


@six.add_metaclass(abc.ABCMeta)
class BaseCommand:
    def __init__(self, api_key, logger=Logger()):
        self.client = self._get_client(api_key, logger)
        self.logger = logger

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def _get_client(self, api_key, logger):
        pass


@six.add_metaclass(abc.ABCMeta)
class ListCommandMixin(object):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

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
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

    @staticmethod
    def _make_list_table(table_data):
        ascii_table = terminaltables.AsciiTable(table_data)
        table_string = ascii_table.table
        return table_string
