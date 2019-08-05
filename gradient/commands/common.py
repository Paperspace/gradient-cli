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
    def _get_table_data(self, experiments):
        pass

    def _log_objects_list(self, objects):
        if not objects:
            self.logger.warning("No data found")
            return

        table_data = self._get_table_data(objects)
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


class CommandBase(object):
    def __init__(self, api=None, logger_=Logger()):
        self.api = api
        self.logger = logger_


class ListCommand(CommandBase):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    @property
    def request_url(self):
        raise NotImplementedError()

    def execute(self, **kwargs):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            response = self._get_response(kwargs)

        try:
            if not response.ok:
                self.logger.log_error_response(response.json())
                return

            objects = self._get_objects(response, kwargs)
        except (ValueError, KeyError) as e:
            self.logger.error("Error while parsing response data: {}".format(e))
        else:
            self._log_objects_list(objects)

    def _log_objects_list(self, objects):
        if not objects:
            self.logger.warning("No data found")
            return

        table_data = self._get_table_data(objects)
        table_str = self._make_table(table_data)
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

    def _get_objects(self, response, kwargs):
        data = response.json()
        return data

    def _get_response(self, kwargs):
        json_ = self._get_request_json(kwargs)
        params = self._get_request_params(kwargs)
        response = self.api.get(self.request_url, json=json_, params=params)
        return response

    def _get_table_data(self, objects):
        raise NotImplementedError()

    @staticmethod
    def _make_table(table_data):
        ascii_table = terminaltables.AsciiTable(table_data)
        table_string = ascii_table.table
        return table_string

    def _get_request_json(self, kwargs):
        return None

    def _get_request_params(self, kwargs):
        return None
