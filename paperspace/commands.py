from pprint import pformat

from paperspace import version, logger
from paperspace.client import API
from paperspace.config import config

default_headers = {"X-API-Key": config.PAPERSPACE_API_KEY,
                   "ps_client_name": "paperspace-python",
                   "ps_client_version": version.version}

experiments_api = API(config.CONFIG_EXPERIMENTS_HOST, headers=default_headers)


def _log_response(response, success_msg, error_msg):
    if response.ok:
        logger.log(success_msg)
    else:
        try:
            data = response.json()
            logger.log_error_response(data)
        except ValueError:
            logger.log(error_msg)


def create_experiments(json, api=experiments_api):
    response = api.post("/experiments/", json=json)
    _log_response(response, "Experiment created", "Unknown error while creating experiment")


def create_and_start_experiments(json, api=experiments_api):
    response = api.post("/experiments/create_and_start/", json=json)
    _log_response(response, "Experiment created", "Unknown error while creating experiment")


def start_experiment(experiment_handle, api=experiments_api):
    url = "/experiments/{}/start/".format(experiment_handle)
    response = api.put(url)
    _log_response(response, "Experiment started", "Unknown error while starting experiment")


def stop_experiment(experiment_handle, api=experiments_api):
    url = "/experiments/{}/stop/".format(experiment_handle)
    response = api.put(url)
    _log_response(response, "Experiment stopped", "Unknown error while stopping experiment")


def list_experiments(api=experiments_api):
    response = api.get("/experiments/")
    _log_response(response, "Experiment stopped", "Unknown error while stopping experiment")


def get_experiment_details(experiment_handle, api=experiments_api):
    url = "/experiments/{}/".format(experiment_handle)
    response = api.get(url)
    details = response.content
    if response.ok:
        try:
            details = pformat(response.json()["data"][0])
        except (ValueError, KeyError, IndexError):
            pass
    _log_response(response, details, "Unknown error while retrieving details of the experiment")
