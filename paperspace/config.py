import json
import os


# TODO: this function is copy-pasted from login.py;
#  there is something weird going one with imports in __init__.py and I'm unable to import apikey now
def apikey():
    paperspace_dir = os.path.expanduser('~/.paperspace')
    config_path = os.path.join(paperspace_dir, 'config.json')
    if os.path.exists(config_path):
        config_data = json.load(open(config_path))
        if config_data and 'apiKey' in config_data:
            return config_data['apiKey']
    return ''


_DEFAULT_PAPERSPACE_API_KEY = apikey()
_DEFAULT_CONFIG_HOST = "https://api.paperspace.io"
_DEFAULT_CONFIG_LOG_HOST = "https://logs.paperspace.io"
_DEFAULT_CONFIG_EXPERIMENTS_HOST = "https://services.paperspace.io/experiments/v1/"  # TODO: validate this


class config(object):
    DEBUG = os.environ.get("PAPERSPACE_CLI_DEBUG") in ("true", "1")
    PAPERSPACE_API_KEY = os.environ.get("PAPERSPACE_API_KEY", _DEFAULT_PAPERSPACE_API_KEY)
    CONFIG_HOST = os.environ.get("PAPERSPACE_CONFIG_HOST", _DEFAULT_CONFIG_HOST)
    CONFIG_LOG_HOST = os.environ.get("PAPERSPACE_CONFIG_LOG_HOST", _DEFAULT_CONFIG_LOG_HOST)
    CONFIG_EXPERIMENTS_HOST = os.environ.get("PAPERSPACE_CONFIG_EXPERIMENTS_HOST", _DEFAULT_CONFIG_EXPERIMENTS_HOST)
