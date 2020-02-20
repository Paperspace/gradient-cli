import abc
import pydoc

import halo
import six
import terminaltables

import gradient.cli_constants
from gradient import api_sdk
from gradient.cliutils import get_terminal_lines
from . import BaseCommand, common


@six.add_metaclass(abc.ABCMeta)
class GetTensorboardClientCommandMixin(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.TensorboardClient(
            api_key=api_key,
            logger=logger,
            ps_client_name=gradient.cli_constants.CLI_PS_CLIENT_NAME,
        )
        return client

    def _log_object(self, instance):
        table_str = self._make_table(instance)
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

        # experiment table
        experiment_table_str = self._make_exp_table(instance)
        if len(experiment_table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(experiment_table_str)
        else:
            self.logger.log(experiment_table_str)

    def _make_table(self, instance):
        """
        :param api_sdk.Tensorboard:
        """
        data = self._get_table_data(instance)
        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string

    def _make_exp_table(self, instance):
        """
        :param api_sdk.Tensorboard:
        """
        data = self._get_exp_table_data(instance)
        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string

    @staticmethod
    def _get_table_data(instance):
        """
        :param api_sdk.Tensorboard instance:
        """
        data = (
            ("ID", instance.id),
            ("Image", instance.image),
            ("URL", instance.url),
            ("State", instance.state),
            # ("Instance type", instance.instance.type),    TODO: for now
            # ("Instance size", instance.instance.size),
            # ("Instance count", instance.instance.count),
        )
        return data

    @staticmethod
    def _get_exp_table_data(instance):
        """
        :param api_sdk.Tensorboard instance:
        """
        data = [["Experiments ID", "State"]]

        for e in instance.experiments:
            data.append([e.get("id"), e.get('state')])
        return data


class CreateTensorboardCommand(GetTensorboardClientCommandMixin, common.BaseCommand):
    SPINNER_MESSAGE = "Creating new tensorboard"

    def execute(self, **kwargs):
        with halo.Halo(text=self.SPINNER_MESSAGE, spinner="dots"):
            notebook_id = self.client.create(**kwargs)

        self.logger.log("Created new tensorboard with id: {}".format(notebook_id))


class GetTensorboardCommand(GetTensorboardClientCommandMixin, common.BaseCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, id_):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instance = self._get_instance(id_)

        self._log_object(instance)

    def _get_instance(self, id_):
        """
        :rtype: api_sdk.Tensorboard
        """
        instance = self.client.get(id_)
        return instance


class ListTensorboardsCommand(GetTensorboardClientCommandMixin, common.ListCommandMixin, common.BaseCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def _get_instances(self, kwargs):
        instances = self.client.list()
        return instances

    def _get_table_data(self, objects):
        # TODO later we need to add information about state
        data = [["ID", "URL", "STATE"]]
        for obj in objects:
            data.append([obj.id, obj.url, obj.state])
        return data


class AddExperimentToTensorboard(GetTensorboardClientCommandMixin, common.BaseCommand):
    SPINNER_MESSAGE = "Adding experiments to tensorboard"

    def execute(self, id, experiments):
        """
        :param str id:
        :param list[str] experiments:
        """
        with halo.Halo(text=self.SPINNER_MESSAGE, spinner="dots"):
            tensorboard = self.client.add_experiments(id, added_experiments=list(experiments))

        self._log_object(tensorboard)


class RemoveExperimentToTensorboard(GetTensorboardClientCommandMixin, common.BaseCommand):
    SPINNER_MESSAGE = "Removing experiments from tensorboard"

    def execute(self, id, **kwargs):
        with halo.Halo(text=self.SPINNER_MESSAGE, spinner="dots"):
            tensorboard = self.client.remove_experiments(id, removed_experiments=list(kwargs.get('experiments')))

        self._log_object(tensorboard)


class DeleteTensorboard(GetTensorboardClientCommandMixin, common.BaseCommand):
    SPINNER_MESSAGE = "Deleting tensorboard"

    def execute(self, *args, **kwargs):
        with halo.Halo(text=self.SPINNER_MESSAGE, spinner="dots"):
            self.client.delete(**kwargs)

        self.logger.log("Delete tensorboard ({}) ended with success".format(kwargs.get("id")))
