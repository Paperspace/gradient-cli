from gradient import config
from gradient.api_sdk.clients import http_client
from .. import logger as sdk_logger


class BaseClient(object):
    API_URL = config.CONFIG_EXPERIMENTS_HOST

    def __init__(self, api_key, logger=sdk_logger.MuteLogger()):
        """

        :type api_key: str
        :type logger: sdk_logger.Logger
        """
        self._client = http_client.API(self.API_URL, api_key=api_key, logger=logger)
        self.logger = logger
