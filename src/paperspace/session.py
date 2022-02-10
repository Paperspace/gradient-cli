from __future__ import annotations
import os
import json


class Session():
    _DEFAULT_CONFIGS = {
        'WEB_URL': 'https://console.paperspace.com',
        'API_HOST': 'https://api.paperspace.com/graphql',
        'CONFIG_HOST': 'https://api.paperspace.io',
        'CONFIG_LOG_HOST': 'https://logs.paperspace.io',
        'CONFIG_EXPERIMENTS_HOST': 'https://services.paperspace.io/experiments/v1/',
        'CONFIG_EXPERIMENTS_HOST_V2': 'https://services.paperspace.io/experiments/v2/',
        'CONFIG_SERVICE_HOST': 'https://services.paperspace.io',
        'CONFIG_DIR_PATH': '~/.paperspace',
        'CONFIG_FILE_NAME': os.path.expanduser('config.json')
    }

    def __init__(self, api_key: str=None) -> None:
        self.config = self.load_configs()
        self.api_key = self.get_api_key(config=self.config, api_key=api_key)

    def load_configs(self) -> dict[str, str]:
        config: dict[str, str] = {}
        for key, val in self._DEFAULT_CONFIGS.items():
            config[key] = os.environ.get(f'PAPERSPACE_{key}', val)

        return config

    def get_api_key(self, config: dict[str, str], api_key: str=None) -> str:
        if api_key is not None:
            return api_key

        if os.environ.get('PAPERSPACE_API_KEY'):
            return os.environ.get('PAPERSPACE_API_KEY')

        paperspace_dir = os.path.expanduser(config['CONFIG_DIR_PATH'])
        config_path = os.path.join(paperspace_dir, config['CONFIG_FILE_NAME'])

        try:
            with open(config_path, 'r') as config_file:
                config_data = json.load(config_file)
        except FileNotFoundError as e:
            print('Unable to locate the Paperspace config file specified')
            print(e)
        return config_data.get('apiKey', '')
