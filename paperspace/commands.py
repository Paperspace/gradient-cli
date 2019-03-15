from paperspace import version, logger
from paperspace.client import API
from paperspace.config import config

default_headers = {"x-api-key": config.PAPERSPACE_API_KEY,
                   "ps_client_name": "paperspace-python",
                   "ps_client_version": version.version}

experiments_api = API(config.CONFIG_EXPERIMENTS_HOST, headers=default_headers)
jobs_api = API(config.CONFIG_HOST, headers=default_headers)


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
    logger.debug(response.content)
    _log_response(response, "Experiment created", "Unknown error while creating experiment")


def create_and_start_experiments(json, api=experiments_api):
    response = api.post("/experiments/create_and_start/", json=json)
    logger.debug(response.content)
    _log_response(response, "Experiment created", "Unknown error while creating experiment")
