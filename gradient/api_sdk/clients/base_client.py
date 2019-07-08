from gradient.config import config
from gradient.api_sdk.clients import http_client
from .. import logger as sdk_logger


class BaseClient(object):
    def __init__(self, api_key, logger=sdk_logger.MuteLogger(), api_url=config.CONFIG_EXPERIMENTS_HOST):
        """

        :type api_key: str
        :type logger: sdk_logger.Logger
        """
        self.api_url = api_url
        self._client = http_client.API(self.api_url, api_key=api_key, logger=logger)
        self.logger = logger
