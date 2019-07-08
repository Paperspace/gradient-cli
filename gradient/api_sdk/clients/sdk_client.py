from gradient.config import config
from .deployment_client import DeploymentsClient
from .experiment_client import ExperimentsClient
from .. import logger as sdk_logger


class SdkClient(object):
    def __init__(self, api_key, logger=sdk_logger.MuteLogger()):
        """

        :type api_key: str
        :type logger: sdk_logger.Logger
        """
        self.experiments = ExperimentsClient(api_key, logger)
        self.deployments = DeploymentsClient(api_key, logger, api_url=config.CONFIG_HOST)
