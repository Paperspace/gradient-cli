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
        Base class. All client classes inherit from it.

        Api Key can be created on paperspace.com after you sign in to your account. Then after obtaining it you can set
        it in CLI using command::
            ``gradient apiKey XXXXXXXXXXXXXXXXXXX``
        or you can include your API key for each command ,for example:: ``gradient experiments run ... --apiKey XXXXXXXXXXXXXXXXXXX``

        :param str api_key: your api token
        :param sdk_logger.Logger logger:
        """
        self.api_key = api_key
        self.client = http_client.API(self.HOST_URL, api_key=api_key, logger=logger)
        self.logger = logger
