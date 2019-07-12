import abc
import pydoc

import six
import terminaltables
from click import style
from halo import halo

from gradient import logger as gradient_logger, constants, api_sdk, exceptions
from gradient.api_sdk.clients import http_client, experiment_client
from gradient.config import config
from gradient.utils import get_terminal_lines

experiments_api = http_client.API(config.CONFIG_EXPERIMENTS_HOST,
                                  headers=http_client.default_headers,
                                  logger=gradient_logger.Logger())


class ExperimentCommand(object):
    def __init__(self, experiments_client, logger_=gradient_logger.Logger()):
        self.experiments_client = experiments_client
        self.logger = logger_


@six.add_metaclass(abc.ABCMeta)
class BaseCreateExperimentCommand(ExperimentCommand):
    SPINNER_MESSAGE = "Creating new experiment"
    CREATE_SUCCESS_MESSAGE_TEMPLATE = "New experiment created with ID: {}"

    def __init__(self, workspace_handler, *args, **kwargs):
        super(BaseCreateExperimentCommand, self).__init__(*args, **kwargs)
        self.workspace_handler = workspace_handler

    def execute(self, json_):
        if "ignore_files" in json_:
            json_["ignore_files"] = self._parse_comma_separated_to_list(json_["ignore_files"])

        self._handle_workspace(json_)

        with halo.Halo(text=self.SPINNER_MESSAGE, spinner="dots"):
            try:
                experiment_id = self._create(json_)
            except api_sdk.GradientSdkError as e:
                self.logger.error(e)
            else:
                self.logger.log(self.CREATE_SUCCESS_MESSAGE_TEMPLATE.format(experiment_id))

    def _handle_workspace(self, instance_dict):
        handler = self.workspace_handler.handle(instance_dict)
        instance_dict.pop("workspace", None)
        instance_dict.pop("workspace_archive", None)
        instance_dict.pop("workspace_url", None)
        if handler:
            instance_dict["workspace_url"] = handler

    @abc.abstractmethod
    def _create(self, json_):
        pass

    @staticmethod
    def _parse_comma_separated_to_list(s):
        if not s:
            return []

        list_of_str = [s.strip() for s in s.split(",")]
        return list_of_str


class CreateSingleNodeExperimentCommand(BaseCreateExperimentCommand):
    def _create(self, json_):
        handle = self.experiments_client.create_single_node(**json_)
        return handle


class CreateMultiNodeExperimentCommand(BaseCreateExperimentCommand):
    def _create(self, json_):
        handle = self.experiments_client.create_multi_node(**json_)
        return handle


class CreateAndStartMultiNodeExperimentCommand(BaseCreateExperimentCommand):
    SPINNER_MESSAGE = "Creating and starting new experiment"
    CREATE_SUCCESS_MESSAGE_TEMPLATE = "New experiment created and started with ID: {}"

    def _create(self, json_):
        handle = self.experiments_client.run_multi_node(**json_)
        return handle


class CreateAndStartSingleNodeExperimentCommand(BaseCreateExperimentCommand):
    SPINNER_MESSAGE = "Creating and starting new experiment"
    CREATE_SUCCESS_MESSAGE_TEMPLATE = "New experiment created and started with ID: {}"

    def _create(self, json_):
        handle = self.experiments_client.run_single_node(**json_)
        return handle


def start_experiment(experiment_id, client, logger_=gradient_logger.Logger()):
    """
    :type experiment_id: str
    :type client: experiment_client.ExperimentsClient
    :param logger_: logger.Logger
    """
    response = client.start(experiment_id)
    logger_.log_response(response, "Experiment started", "Unknown error while starting the experiment")


def stop_experiment(experiment_id, client, logger_=gradient_logger.Logger()):
    """
    :type experiment_id: str
    :type client: experiment_client.ExperimentsClient
    :param logger_: logger.Logger
    """
    response = client.stop(experiment_id)
    logger_.log_response(response, "Experiment stopped", "Unknown error while stopping the experiment")


class ListExperimentsCommand(ExperimentCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, **kwargs):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instances = self._get_instances(kwargs)

        self._log_objects_list(instances)

    def _get_instances(self, kwargs):
        project_id = kwargs.get("project_id")
        try:
            instances = self.experiments_client.list(project_id)
        except api_sdk.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instances

    @staticmethod
    def _get_table_data(experiments):
        data = [("Name", "ID", "Status")]
        for experiment in experiments:
            name = experiment.name
            handle = experiment.id
            status = constants.ExperimentState.get_state_str(experiment.state)
            data.append((name, handle, status))

        return data

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


class GetExperimentCommand(ExperimentCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, **kwargs):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instance = self._get_instance(kwargs)

        self._log_object(instance)

    def _get_instance(self, kwargs):
        """
        :rtype: api_sdk.SingleNodeExperiment|api_sdk.MultiNodeExperiment
        """
        experiment_id = kwargs["experiment_id"]
        try:
            instance = self.experiments_client.get(experiment_id)
        except api_sdk.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instance

    def _log_object(self, instance):

        table_str = self._make_table(instance)
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

    @staticmethod
    def _make_table(experiment):
        if experiment.experiment_type_id == constants.ExperimentType.SINGLE_NODE:
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
        elif experiment.experiment_type_id in (constants.ExperimentType.GRPC_MULTI_NODE,
                                               constants.ExperimentType.MPI_MULTI_NODE):
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
        else:
            raise ValueError("Wrong experiment type: {}".format(experiment.experiment_type_id))

        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string


class ExperimentLogsCommand(ExperimentCommand):
    def execute(self, experiment_id, line, limit, follow):
        if follow:
            self.logger.log("Awaiting logs...")
            self._log_logs_continuously(experiment_id, line, limit)
        else:
            self._log_table_of_logs(experiment_id, line, limit)

    def _log_table_of_logs(self, experiment_id, line, limit):
        logs = self.experiments_client.logs(experiment_id, line, limit)
        if not logs:
            self.logger.log("No logs found")
            return

        table_str = self._make_table(logs, experiment_id)
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

    def _log_logs_continuously(self, experiment_id, line, limit):
        logs_gen = self.experiments_client.yield_logs(experiment_id, line, limit)
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
