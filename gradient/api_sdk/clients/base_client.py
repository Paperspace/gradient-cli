from gradient.config import config
from .. import logger as sdk_logger
from ..clients import http_client


class BaseClient(object):
    HOST_URL = config.CONFIG_EXPERIMENTS_HOST

    def __init__(
            self, api_key,
            logger=sdk_logger.MuteLogger()
    ):
        """

        :param str api_key:
        :param sdk_logger.Logger logger:
        """
        self.api_key = api_key
        self.client = http_client.API(self.HOST_URL, api_key=api_key, logger=logger)
        self.logger = logger
