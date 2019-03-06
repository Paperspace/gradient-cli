from paperspace import config, version, logger

from paperspace.client import API

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


def create_experiments(json=None, api=experiments_api):
    json = json or {}
    response = api.post("/experiments/", json=json, params={"accessToken": config.PAPERSPACE_API_KEY})
    _log_response(response, "Experiment created", "Unknown error while creating experiment")
