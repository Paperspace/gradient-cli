from gradient.config import config
from .. import logger as sdk_logger
from ..clients import http_client


class BaseClient(object):
    def __init__(
            self, api_key,
            logger=sdk_logger.MuteLogger(),
            api_url=config.CONFIG_EXPERIMENTS_HOST,
    ):
        """

        :param str api_key:
        :param sdk_logger.Logger logger:
        :param str api_url:
        """
        self.api_key = api_key
        self.api_url = api_url
        self.client = http_client.API(self.api_url, api_key=api_key, logger=logger)
        self.logger = logger
