import pydoc

import terminaltables

from paperspace import version, logger, constants, client
from paperspace.config import config
from paperspace.utils import get_terminal_lines

default_headers = {"X-API-Key": config.PAPERSPACE_API_KEY,
                   "ps_client_name": "paperspace-python",
                   "ps_client_version": version.version}

experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, headers=default_headers)


def _log_response(response, success_msg, error_msg, logger_=logger):
    if response.ok:
        logger_.log(success_msg)
    else:
        try:
            data = response.json()
            logger_.log_error_response(data)
        except ValueError:
            logger_.log(error_msg)


def _log_create_experiment(response, success_msg_template, error_msg, logger_=logger):
    if response.ok:
        j = response.json()
        handle = j["handle"]
        msg = success_msg_template.format(handle)
        logger_.log(msg)
    else:
        try:
            data = response.json()
            logger_.log_error_response(data)
        except ValueError:
            logger_.log(error_msg)


def create_experiment(json_, api=experiments_api):
    response = api.post("/experiments/", json=json_)

    _log_create_experiment(response,
                           "New experiment created with handle: {}",
                           "Unknown error while creating the experiment")


def create_and_start_experiment(json_, api=experiments_api):
    response = api.post("/experiments/create_and_start/", json=json_)
    _log_create_experiment(response,
                           "New experiment created and started with handle: {}",
                           "Unknown error while creating/starting the experiment")


def start_experiment(experiment_handle, api=experiments_api):
    url = "/experiments/{}/start/".format(experiment_handle)
    response = api.put(url)
    _log_response(response, "Experiment started", "Unknown error while starting the experiment")


def stop_experiment(experiment_handle, api=experiments_api):
    url = "/experiments/{}/stop/".format(experiment_handle)
    response = api.put(url)
    _log_response(response, "Experiment stopped", "Unknown error while stopping the experiment")


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


def list_experiments(api=experiments_api):
    # TODO: change to limit: -1 when PS-9535 is deployed to production
    response = api.get("/experiments/", params={"limit": 1000000})
    details = response.content
    if response.ok:
        try:
            experiments = response.json()["data"]
            details = _make_experiments_list_table(experiments)
        except (ValueError, KeyError) as e:
            logger.log("Error parsing response data")
            logger.debug(e)

    if response.ok and len(details.splitlines()) > get_terminal_lines():
        pydoc.pager(details)
    else:
        _log_response(response, details, "Unknown error while retrieving list of experiments")


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
            logger.log("Error parsing response data")
            logger.debug(e)

    _log_response(response, details, "Unknown error while retrieving details of the experiment")
