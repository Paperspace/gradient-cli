import abc
import pydoc

import six
import terminaltables
from click import style
from halo import halo

from gradient import logger as gradient_logger, constants, config, api_sdk, exceptions
from gradient.api_sdk.clients import http_client, sdk_client
from gradient.commands import common
from gradient.utils import get_terminal_lines
from gradient.workspace import S3WorkspaceHandler

experiments_api = http_client.API(config.CONFIG_EXPERIMENTS_HOST,
                                  headers=http_client.default_headers,
                                  logger=gradient_logger.Logger())


class ExperimentCommand(common.CommandBase):
    def __init__(self, workspace_handler=None, **kwargs):
        super(ExperimentCommand, self).__init__(**kwargs)
        self._workspace_handler = workspace_handler or S3WorkspaceHandler(experiments_api=self.api, logger_=self.logger)

    def _log_create_experiment(self, response, success_msg_template, error_msg):
        if response.ok:
            j = response.json()
            id_ = j["handle"]
            msg = success_msg_template.format(id_)
            self.logger.log(msg)
        else:
            try:
                data = response.json()
                self.logger.log_error_response(data)
            except ValueError:
                self.logger.error(error_msg)


@six.add_metaclass(abc.ABCMeta)
class _CreateExperimentCommand(object):
    def __init__(self, sdk_client, logger_=gradient_logger.Logger()):
        self.sdk_client = sdk_client
        self.logger = logger_

    def execute(self, json_):
        if "ignore_files" in json_:
            json_["ignore_files"] = self._parse_comma_separated_to_list(json_["ignore_files"])

        with halo.Halo(text="Creating new experiment", spinner="dots"):
            try:
                experiment_id = self._create(json_)
            except api_sdk.GradientSdkError as e:
                self.logger.error(e)
            else:
                self.logger.log("New experiment created with ID: {}".format(experiment_id))

    @abc.abstractmethod
    def _create(self, json_):
        pass

    @staticmethod
    def _parse_comma_separated_to_list(s):
        if not s:
            return []

        list_of_str = [s.strip() for s in s.split(",")]
        return list_of_str


class CreateSingleNodeExperimentCommand(_CreateExperimentCommand):
    def _create(self, json_):
        handle = self.sdk_client.experiments.create_single_node(**json_)
        return handle


class CreateMultiNodeExperimentCommand(_CreateExperimentCommand):
    def _create(self, json_):
        handle = self.sdk_client.experiments.create_multi_node(**json_)
        return handle


@six.add_metaclass(abc.ABCMeta)
class _RunExperimentCommand(object):
    def __init__(self, sdk_client, logger_=gradient_logger.Logger()):
        self.sdk_client = sdk_client
        self.logger = logger_

    def execute(self, json_):
        with halo.Halo(text="Creating and starting new experiment", spinner="dots"):
            try:
                experiment_id = self._create(json_)
            except api_sdk.GradientSdkError as e:
                self.logger.error(e)
            else:
                self.logger.log("New experiment created and started with ID: {}".format(experiment_id))

    @abc.abstractmethod
    def _create(self, json_):
        pass


class CreateAndStartMultiNodeExperimentCommand(_RunExperimentCommand):
    def _create(self, json_):
        handle = self.sdk_client.experiments.run_multi_node(**json_)
        return handle


class CreateAndStartSingleNodeExperimentCommand(_RunExperimentCommand):
    def _create(self, json_):
        handle = self.sdk_client.experiments.run_single_node(**json_)
        return handle


def start_experiment(experiment_id, client, logger_=gradient_logger.Logger()):
    """
    :type experiment_id: str
    :type client: sdk_client.SdkClient
    :param logger_: logger.Logger
    """
    response = client.experiments.start(experiment_id)
    logger_.log_response(response, "Experiment started", "Unknown error while starting the experiment")


def stop_experiment(experiment_id, client, logger_=gradient_logger.Logger()):
    """
    :type experiment_id: str
    :type client: sdk_client.SdkClient
    :param logger_: logger.Logger
    """
    response = client.experiments.start(experiment_id)
    logger_.log_response(response, "Experiment stopped", "Unknown error while stopping the experiment")


class ListExperimentsCommand(object):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def __init__(self, client, logger=gradient_logger.Logger()):
        """

        :type client: sdk_client.SdkClient
        """
        self.client = client
        self.logger = logger

    def execute(self, **kwargs):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instances = self._get_instances(kwargs)

        self._log_objects_list(instances)

    def _get_instances(self, kwargs):
        project_id = kwargs.get("project_id")
        try:
            instances = self.client.experiments.list(project_id)
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


def _make_details_table(experiment):
    if experiment["experimentTypeId"] == constants.ExperimentType.SINGLE_NODE:
        data = (
            ("Name", experiment["templateHistory"]["params"].get("name")),
            ("ID", experiment.get("handle")),
            ("State", constants.ExperimentState.get_state_str(experiment.get("state"))),
            ("Ports", experiment["templateHistory"]["params"].get("ports")),
            ("Project ID", experiment["templateHistory"]["params"].get("project_handle")),
            ("Worker Command", experiment["templateHistory"]["params"].get("worker_command")),
            ("Worker Container", experiment["templateHistory"]["params"].get("worker_container")),
            ("Worker Machine Type", experiment["templateHistory"]["params"].get("worker_machine_type")),
            ("Working Directory", experiment["templateHistory"]["params"].get("workingDirectory")),
            ("Workspace URL", experiment["templateHistory"]["params"].get("workspaceUrl")),
            ("Model Type", experiment["templateHistory"]["params"].get("modelType")),
            ("Model Path", experiment["templateHistory"]["params"].get("modelPath")),
        )
    elif experiment["experimentTypeId"] in (constants.ExperimentType.GRPC_MULTI_NODE,
                                            constants.ExperimentType.MPI_MULTI_NODE):
        data = (
            ("Name", experiment["templateHistory"]["params"].get("name")),
            ("ID", experiment.get("handle")),
            ("State", constants.ExperimentState.get_state_str(experiment.get("state"))),
            ("Artifact directory", experiment["templateHistory"]["params"].get("artifactDirectory")),
            ("Cluster ID", experiment["templateHistory"]["params"].get("clusterId")),
            ("Experiment Env", experiment["templateHistory"]["params"].get("experimentEnv")),
            ("Experiment Type",
             constants.ExperimentType.get_type_str(experiment["templateHistory"]["params"].get("experimentTypeId"))),
            ("Model Type", experiment["templateHistory"]["params"].get("modelType")),
            ("Model Path", experiment["templateHistory"]["params"].get("modelPath")),
            ("Parameter Server Command", experiment["templateHistory"]["params"].get("parameter_server_command")),
            ("Parameter Server Container", experiment["templateHistory"]["params"].get("parameter_server_container")),
            ("Parameter Server Count", experiment["templateHistory"]["params"].get("parameter_server_count")),
            ("Parameter Server Machine Type",
             experiment["templateHistory"]["params"].get("parameter_server_machine_type")),
            ("Ports", experiment["templateHistory"]["params"].get("ports")),
            ("Project ID", experiment["templateHistory"]["params"].get("project_handle")),
            ("Worker Command", experiment["templateHistory"]["params"].get("worker_command")),
            ("Worker Container", experiment["templateHistory"]["params"].get("worker_container")),
            ("Worker Count", experiment["templateHistory"]["params"].get("worker_count")),
            ("Worker Machine Type", experiment["templateHistory"]["params"].get("worker_machine_type")),
            ("Working Directory", experiment["templateHistory"]["params"].get("workingDirectory")),
            ("Workspace URL", experiment["templateHistory"]["params"].get("workspaceUrl")),
        )
    else:
        raise ValueError("Wrong experiment type: {}".format(experiment["experimentTypeId"]))

    ascii_table = terminaltables.AsciiTable(data)
    table_string = ascii_table.table
    return table_string


def get_experiment_details(experiment_id, api=experiments_api, logger_=gradient_logger.Logger()):
    url = "/experiments/{}/".format(experiment_id)
    response = api.get(url)
    details = response.content
    if response.ok:
        try:
            experiment = response.json()["data"]
            details = _make_details_table(experiment)
        except (ValueError, KeyError) as e:
            logger_.error("Error parsing response data")

    logger_.log_response(response, details, "Unknown error while retrieving details of the experiment")


class ExperimentLogsCommand(common.CommandBase):
    last_line_number = 0
    base_url = "/jobs/logs"

    is_logs_complete = False

    def execute(self, experiment_id, line, limit, follow):
        if follow:
            self.logger.log("Awaiting logs...")

        self.last_line_number = line
        table_title = "Experiment %s logs" % experiment_id
        table_data = [("JOB ID", "LINE", "MESSAGE")]
        table = terminaltables.AsciiTable(table_data, title=table_title)

        while not self.is_logs_complete:
            response = self._get_logs(experiment_id, self.last_line_number, limit)

            try:
                data = response.json()
                if not response.ok:
                    self.logger.log_error_response(data)
                    return
            except (ValueError, KeyError) as e:
                if response.status_code == 204:
                    continue
                self.logger.log("Error while parsing response data: {}".format(e))
                return
            else:
                self._log_logs_list(data, table, table_data, follow)

            if not follow:
                self.is_logs_complete = True

    def _get_logs(self, experiment_id, line, limit):
        params = {
            'experimentId': experiment_id,
            'line': line,
            'limit': limit
        };
        return self.api.get(self.base_url, params=params)

    def _log_logs_list(self, data, table, table_data, follow):
        if not data:
            self.logger.log("No logs found")
            return
        if follow:
            # TODO track number of jobs seen to look for PSEOF
            if data[-1].get("message") == "PSEOF":
                self.is_logs_complete = True
            else:
                self.last_line_number = data[-1].get("line")
            for log in data:
                log_str = "{}\t{}\t{}"
                self.logger.log(log_str.format(style(fg="blue", text=str(log.get("jobId"))), style(fg="red", text=str(log.get("line"))), log.get("message")))
        else:
            table_str = self._make_table(data, table, table_data)
            if len(table_str.splitlines()) > get_terminal_lines():
                pydoc.pager(table_str)
            else:
                self.logger.log(table_str)

    def _make_table(self, logs, table, table_data):
        if logs[-1].get("message") == "PSEOF":
            self.is_logs_complete = True
        else:
            self.last_line_number = logs[-1].get("line")

        for log in logs:
            table_data.append((style(fg="blue", text=str(log.get("jobId"))), style(fg="red", text=str(log.get("line"))), log.get("message")))

        return table.table
