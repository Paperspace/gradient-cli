import json
import os


# TODO: this function is copy-pasted from login.py;
#  there is something weird going one with imports in __init__.py and I'm unable to import apikey now
def get_api_key(config_dir_path, config_file_name):
    paperspace_dir = os.path.expanduser(config_dir_path)
    config_path = os.path.join(paperspace_dir, config_file_name)
    if os.path.exists(config_path):
        config_data = json.load(open(config_path))
        if config_data and 'apiKey' in config_data:
            return config_data['apiKey']
    return ''


_DEFAULT_WEB_URL = "https://www.paperspace.com"
_DEFAULT_CONFIG_HOST = "https://api.paperspace.io"
_DEFAULT_CONFIG_LOG_HOST = "https://logs.paperspace.io"
_DEFAULT_CONFIG_EXPERIMENTS_HOST = "https://services.paperspace.io/experiments/v1/"
_DEFAULT_CONFIG_EXPERIMENTS_HOST_V2 = "https://services.paperspace.io/experiments/v2/"
_DEFAULT_CONFIG_SERVICE_HOST = "https://services.paperspace.io"
_DEFAULT_CONFIG_DIR_PATH = "~/.paperspace"
_DEFAULT_CONFIG_FILE_NAME = os.path.expanduser("config.json")
_DEFAULT_HELP_HEADERS_COLOR = "yellow"
_DEFAULT_HELP_OPTIONS_COLOR = "green"
_DEFAULT_USE_CONSOLE_COLORS = True


def get_help_colors_dict(use_colors, help_headers_color, help_options_color):
    if not use_colors:
        return {}

    d = {
        "help_headers_color": help_headers_color,
        "help_options_color": help_options_color,
    }
    return d


class config(object):
    DEBUG = os.environ.get("PAPERSPACE_CLI_DEBUG") in ("true", "1")

    WEB_URL = os.environ.get("PAPERSPACE_WEB_URL", _DEFAULT_WEB_URL)
    CONFIG_HOST = os.environ.get("PAPERSPACE_CONFIG_HOST", _DEFAULT_CONFIG_HOST)
    CONFIG_LOG_HOST = os.environ.get("PAPERSPACE_CONFIG_LOG_HOST", _DEFAULT_CONFIG_LOG_HOST)
    CONFIG_EXPERIMENTS_HOST = os.environ.get("PAPERSPACE_CONFIG_EXPERIMENTS_HOST", _DEFAULT_CONFIG_EXPERIMENTS_HOST)
    CONFIG_EXPERIMENTS_HOST_V2 = os.environ.get("PAPERSPACE_CONFIG_EXPERIMENTS_HOST_V2",
                                                _DEFAULT_CONFIG_EXPERIMENTS_HOST_V2)
    CONFIG_SERVICE_HOST = os.environ.get("PAPERSPACE_CONFIG_SERVICE_HOST", _DEFAULT_CONFIG_SERVICE_HOST)
    CONFIG_DIR_PATH = os.path.expanduser(os.environ.get("PAPERSPACE_CONFIG_PATH", _DEFAULT_CONFIG_DIR_PATH))
    CONFIG_FILE_NAME = os.environ.get("PAPERSPACE_CONFIG_FILE_NAME", _DEFAULT_CONFIG_FILE_NAME)
    PAPERSPACE_API_KEY = os.environ.get("PAPERSPACE_API_KEY", get_api_key(CONFIG_DIR_PATH, CONFIG_FILE_NAME))

    HELP_HEADERS_COLOR = os.environ.get("PAPERSPACE_HELP_HEADERS_COLOR", _DEFAULT_HELP_HEADERS_COLOR)
    HELP_OPTIONS_COLOR = os.environ.get("PAPERSPACE_HELP_OPTIONS_COLOR", _DEFAULT_HELP_OPTIONS_COLOR)
    USE_CONSOLE_COLORS = os.environ.get("PAPERSPACE_USE_CONSOLE_COLORS",
                                        _DEFAULT_USE_CONSOLE_COLORS) in (True, "true", "1")
    HELP_COLORS_DICT = get_help_colors_dict(USE_CONSOLE_COLORS, HELP_HEADERS_COLOR, HELP_OPTIONS_COLOR)
