import pydoc

import terminaltables

from paperspace import logger, constants, client, config
from paperspace.commands import CommandBase
from paperspace.workspace import S3WorkspaceHandler
from paperspace.logger import log_response
from paperspace.utils import get_terminal_lines

experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, headers=client.default_headers)


class ExperimentCommand(CommandBase):
    def __init__(self, workspace_handler=None, **kwargs):
        super(ExperimentCommand, self).__init__(**kwargs)
        self._workspace_handler = workspace_handler or S3WorkspaceHandler(experiments_api=self.api, logger=self.logger)

    def _log_create_experiment(self, response, success_msg_template, error_msg):
        if response.ok:
            j = response.json()
            handle = j["handle"]
            msg = success_msg_template.format(handle)
            self.logger.log(msg)
        else:
            try:
                data = response.json()
                self.logger.log_error_response(data)
            except ValueError:
                self.logger.error(error_msg)


class CreateExperimentCommand(ExperimentCommand):

    def execute(self, json_):
        workspace_url = self._workspace_handler.upload_workspace(json_)
        if workspace_url:
            json_['workspaceUrl'] = workspace_url

        response = self.api.post("/experiments/", json=json_)

        self._log_create_experiment(response,
                                    "New experiment created with handle: {}",
                                    "Unknown error while creating the experiment")


class CreateAndStartExperimentCommand(ExperimentCommand):
    def execute(self, json_):
        workspace_url = self._workspace_handler.upload_workspace(json_)
        if workspace_url:
            json_['workspaceUrl'] = workspace_url

        response = self.api.post("/experiments/create_and_start/", json=json_)
        self._log_create_experiment(response,
                                    "New experiment created and started with handle: {}",
                                    "Unknown error while creating/starting the experiment")


def start_experiment(experiment_handle, api=experiments_api):
    url = "/experiments/{}/start/".format(experiment_handle)
    response = api.put(url)
    log_response(response, "Experiment started", "Unknown error while starting the experiment")


def stop_experiment(experiment_handle, api=experiments_api):
    url = "/experiments/{}/stop/".format(experiment_handle)
    response = api.put(url)
    log_response(response, "Experiment stopped", "Unknown error while stopping the experiment")


class ListExperimentsCommand(object):
    def __init__(self, api=experiments_api, logger_=logger):
        self.api = api
        self.logger = logger_

    def execute(self, project_handles=None):
        project_handles = project_handles or []
        params = self._get_query_params(project_handles)
        response = self.api.get("/experiments/", params=params)

        try:
            data = response.json()
            if not response.ok:
                self.logger.log_error_response(data)
                return

            experiments = self._get_experiments_list(data, bool(project_handles))
        except (ValueError, KeyError) as e:
            self.logger.error("Error while parsing response data: {}".format(e))
        else:
            self._log_experiments_list(experiments)

    @staticmethod
    def _get_query_params(project_handles):
        params = {"limit": -1}  # so the API sends back full list without pagination
        for i, handle in enumerate(project_handles):
            key = "projectHandle[{}]".format(i)
            params[key] = handle

        return params

    @staticmethod
    def _make_experiments_list_table(experiments):
        data = [("Name", "Handle", "Status")]
        for experiment in experiments:
            name = experiment["templateHistory"]["params"].get("name")
            handle = experiment["handle"]
            status = constants.ExperimentState.get_state_str(experiment["state"])
            data.append((name, handle, status))

        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string

    @staticmethod
    def _get_experiments_list(data, filtered=False):
        if not filtered:  # If filtering by projectHandle response data has different format...
            return data["data"]

        experiments = []
        for project_experiments in data["data"]:
            for experiment in project_experiments["data"]:
                experiments.append(experiment)
        return experiments

    def _log_experiments_list(self, experiments):
        if not experiments:
            self.logger.warning("No experiments found")
        else:
            table_str = self._make_experiments_list_table(experiments)
            if len(table_str.splitlines()) > get_terminal_lines():
                pydoc.pager(table_str)
            else:
                self.logger.log(table_str)


def _make_details_table(experiment):
    if experiment["experimentTypeId"] == constants.ExperimentType.SINGLE_NODE:
        data = (
            ("Name", experiment["templateHistory"]["params"].get("name")),
            ("Handle", experiment.get("handle")),
            ("State", constants.ExperimentState.get_state_str(experiment.get("state"))),
            ("Ports", experiment["templateHistory"]["params"].get("ports")),
            ("Project Handle", experiment["templateHistory"]["params"].get("project_handle")),
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
            ("Handle", experiment.get("handle")),
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
            ("Project Handle", experiment["templateHistory"]["params"].get("project_handle")),
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


def get_experiment_details(experiment_handle, api=experiments_api):
    url = "/experiments/{}/".format(experiment_handle)
    response = api.get(url)
    details = response.content
    if response.ok:
        try:
            experiment = response.json()["data"]
            details = _make_details_table(experiment)
        except (ValueError, KeyError) as e:
            logger.error("Error parsing response data")

    log_response(response, details, "Unknown error while retrieving details of the experiment")
