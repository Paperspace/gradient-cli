import abc
import pydoc

import six
import terminaltables
from click import style
from halo import halo

from gradient import constants, api_sdk, exceptions
from gradient.commands.common import BaseCommand, ListCommandMixin
from gradient.utils import get_terminal_lines


@six.add_metaclass(abc.ABCMeta)
class BaseExperimentCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.ExperimentsClient(api_key=api_key, logger=logger)
        return client


@six.add_metaclass(abc.ABCMeta)
class BaseCreateExperimentCommandMixin(object):
    SPINNER_MESSAGE = "Creating new experiment"
    CREATE_SUCCESS_MESSAGE_TEMPLATE = "New experiment created with ID: {}"

    def __init__(self, workspace_handler, *args, **kwargs):
        super(BaseCreateExperimentCommandMixin, self).__init__(*args, **kwargs)
        self.workspace_handler = workspace_handler

    def execute(self, json_, use_vpc=False):
        if "ignore_files" in json_:
            json_["ignore_files"] = self._parse_comma_separated_to_list(json_["ignore_files"])

        self._handle_workspace(json_)

        with halo.Halo(text=self.SPINNER_MESSAGE, spinner="dots"):
            try:
                experiment_id = self._create(json_, use_vpc=use_vpc)
            except api_sdk.GradientSdkError as e:
                self.logger.error(e)
                return

        self.logger.log(self.CREATE_SUCCESS_MESSAGE_TEMPLATE.format(experiment_id))
        return experiment_id

    def _handle_workspace(self, instance_dict):
        handler = self.workspace_handler.handle(instance_dict)
        instance_dict.pop("ignore_files", None)
        instance_dict.pop("workspace", None)
        instance_dict.pop("workspace_archive", None)
        instance_dict.pop("workspace_url", None)
        if handler and handler != "none":
            instance_dict["workspace_url"] = handler

    @abc.abstractmethod
    def _create(self, json_, use_vpc):
        pass

    @staticmethod
    def _parse_comma_separated_to_list(s):
        if not s:
            return []

        list_of_str = [s.strip() for s in s.split(",")]
        return list_of_str


class CreateSingleNodeExperimentCommand(BaseCreateExperimentCommandMixin, BaseExperimentCommand):
    def _create(self, json_, use_vpc=False):
        handle = self.client.create_single_node(use_vpc=use_vpc, **json_)
        return handle


class CreateMultiNodeExperimentCommand(BaseCreateExperimentCommandMixin, BaseExperimentCommand):
    def _create(self, json_, use_vpc=False):
        handle = self.client.create_multi_node(use_vpc=use_vpc, **json_)
        return handle


class CreateAndStartMultiNodeExperimentCommand(BaseCreateExperimentCommandMixin, BaseExperimentCommand):
    SPINNER_MESSAGE = "Creating and starting new experiment"
    CREATE_SUCCESS_MESSAGE_TEMPLATE = "New experiment created and started with ID: {}"

    def _create(self, json_, use_vpc=False):
        handle = self.client.run_multi_node(use_vpc=use_vpc, **json_)
        return handle


class CreateAndStartSingleNodeExperimentCommand(BaseCreateExperimentCommandMixin, BaseExperimentCommand):
    SPINNER_MESSAGE = "Creating and starting new experiment"
    CREATE_SUCCESS_MESSAGE_TEMPLATE = "New experiment created and started with ID: {}"

    def _create(self, json_, use_vpc=False):
        handle = self.client.run_single_node(use_vpc=use_vpc, **json_)
        return handle


class StartExperimentCommand(BaseExperimentCommand):
    def execute(self, experiment_id, use_vpc=False):
        """
        :param str experiment_id:
        :param bool use_vpc:
        """
        self.client.start(experiment_id, use_vpc=use_vpc)
        self.logger.log("Experiment started")


class StopExperimentCommand(BaseExperimentCommand):
    def execute(self, experiment_id, use_vpc=False):
        """
        :param str experiment_id:
        :param str use_vpc:
        """
        self.client.stop(experiment_id, use_vpc=use_vpc)
        self.logger.log("Experiment stopped")


class ListExperimentsCommand(ListCommandMixin, BaseExperimentCommand):
    def _get_instances(self, kwargs):
        project_id = kwargs.get("project_id")
        try:
            instances = self.client.list(project_id)
        except api_sdk.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instances

    def _get_table_data(self, experiments):
        data = [("Name", "ID", "Status")]
        for experiment in experiments:
            name = experiment.name
            handle = experiment.id
            status = constants.ExperimentState.get_state_str(experiment.state)
            data.append((name, handle, status))

        return data


class GetExperimentCommand(BaseExperimentCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, id_):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instance = self._get_instance(id_)

        self._log_object(instance)

    def _get_instance(self, id_):
        """
        :rtype: api_sdk.SingleNodeExperiment|api_sdk.MultiNodeExperiment
        """
        try:
            instance = self.client.get(id_)
        except api_sdk.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instance

    def _log_object(self, instance):

        table_str = self._make_table(instance)
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

    def _make_table(self, experiment):
        """
        :param api_sdk.BaseExperiment:
        """
        data = self._get_experiment_table_data(experiment)
        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string

    def _get_experiment_table_data(self, experiment):
        if experiment.experiment_type_id == constants.ExperimentType.SINGLE_NODE:
            return self._get_single_node_data(experiment)

        if experiment.experiment_type_id in (constants.ExperimentType.GRPC_MULTI_NODE,
                                             constants.ExperimentType.MPI_MULTI_NODE):
            return self._get_multi_node_data(experiment)

        raise ValueError("Wrong experiment type: {}".format(experiment.experiment_type_id))

    @staticmethod
    def _get_single_node_data(experiment):
        """
        :param api_sdk.SingleNodeExperiment experiment:
        """
        data = (
            ("Name", experiment.name),
            ("ID", experiment.id),
            ("State", constants.ExperimentState.get_state_str(experiment.state)),
            ("Ports", experiment.ports),
            ("Project ID", experiment.project_id),
            ("Worker Command", experiment.command),
            ("Worker Container", experiment.container),
            ("Worker Machine Type", experiment.machine_type),
            ("Working Directory", experiment.working_directory),
            ("Workspace URL", experiment.workspace_url),
            ("Model Type", experiment.model_type),
            ("Model Path", experiment.model_path),
        )
        return data

    @staticmethod
    def _get_multi_node_data(experiment):
        """
        :param api_sdk.MultiNodeExperiment experiment:
        """
        data = (
            ("Name", experiment.name),
            ("ID", experiment.id),
            ("State", constants.ExperimentState.get_state_str(experiment.state)),
            ("Artifact directory", experiment.artifact_directory),
            ("Cluster ID", experiment.cluster_id),
            ("Experiment Env", experiment.experiment_env),
            ("Experiment Type", constants.ExperimentType.get_type_str(experiment.experiment_type_id)),
            ("Model Type", experiment.model_type),
            ("Model Path", experiment.model_path),
            ("Parameter Server Command", experiment.parameter_server_command),
            ("Parameter Server Container", experiment.parameter_server_container),
            ("Parameter Server Count", experiment.parameter_server_count),
            ("Parameter Server Machine Type", experiment.parameter_server_machine_type),
            ("Ports", experiment.ports),
            ("Project ID", experiment.project_id),
            ("Worker Command", experiment.worker_command),
            ("Worker Container", experiment.worker_container),
            ("Worker Count", experiment.worker_count),
            ("Worker Machine Type", experiment.worker_machine_type),
            ("Working Directory", experiment.working_directory),
            ("Workspace URL", experiment.workspace_url),
        )
        return data


class ExperimentLogsCommand(BaseExperimentCommand):
    def execute(self, experiment_id, line, limit, follow):
        if follow:
            self.logger.log("Awaiting logs...")
            self._log_logs_continuously(experiment_id, line, limit)
        else:
            self._log_table_of_logs(experiment_id, line, limit)

    def _log_table_of_logs(self, experiment_id, line, limit):
        logs = self.client.logs(experiment_id, line, limit)
        if not logs:
            self.logger.log("No logs found")
            return

        table_str = self._make_table(logs, experiment_id)
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

    def _log_logs_continuously(self, experiment_id, line, limit):
        logs_gen = self.client.yield_logs(experiment_id, line, limit)
        for log in logs_gen:
            log_msg = "{}\t{}\t{}".format(*self._format_row(experiment_id, log))
            self.logger.log(log_msg)

    def _make_table(self, logs, experiment_id):
        table_title = "Experiment %s logs" % experiment_id
        table_data = [("JOB ID", "LINE", "MESSAGE")]
        table = terminaltables.AsciiTable(table_data, title=table_title)

        for log in logs:
            table_data.append(self._format_row(experiment_id, log))

        return table.table

    @staticmethod
    def _format_row(experiment_id, log_row):
        return (style(fg="blue", text=experiment_id),
                style(fg="red", text=str(log_row.line)),
                log_row.message)
