from . import DeploymentsClient, ExperimentsClient, HyperparameterJobsClient, ModelsClient
from .. import logger as sdk_logger


class SdkClient(object):
    def __init__(self, api_key, logger=sdk_logger.MuteLogger()):
        """
        :param str api_key: api Key
        :param sdk_logger.Logger logger:
        """
        self.experiments = ExperimentsClient(api_key=api_key, logger=logger)
        self.deployments = DeploymentsClient(api_key=api_key, logger=logger)
        self.hyperparameters = HyperparameterJobsClient(api_key=api_key, logger=logger)
        self.models = ModelsClient(api_key=api_key, logger=logger)
