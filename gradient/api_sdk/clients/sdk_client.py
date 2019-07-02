from .experiment_client import ExperimentsClient
from .. import logger as sdk_logger


class SdkClient(object):
    def __init__(self, api_key, logger=sdk_logger.MuteLogger()):
        """

        :type api_key: str
        :type logger: sdk_logger.Logger
        """
        self.experiments = ExperimentsClient(api_key, logger)
