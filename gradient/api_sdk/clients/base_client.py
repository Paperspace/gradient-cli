from gradient import config
from gradient.api_sdk.clients import api_client
from .. import logger as sdk_logger


class BaseClient(object):
    API_URL = config.CONFIG_EXPERIMENTS_HOST

    def __init__(self, api_key, logger=sdk_logger.MuteLogger()):
        """

        :type api_key: str
        :type logger: sdk_logger.Logger
        """
        self._client = api_client.API(self.API_URL, api_key=api_key)
        self.logger = logger
