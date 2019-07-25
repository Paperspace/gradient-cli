from . import DeploymentsClient, ExperimentsClient, HyperparameterJobsClient, ModelsClient
from gradient.config import config
from .job_client import JobsClient
from .. import logger as sdk_logger


class SdkClient(object):
    def __init__(self, api_key, logger=sdk_logger.MuteLogger(), vpc=False):
        """
        :param str api_key:
        :param sdk_logger.Logger logger:
        """
        self.experiments = ExperimentsClient(api_key=api_key, logger=logger, vpc=vpc)
        self.deployments = DeploymentsClient(api_key=api_key, logger=logger)
        self.hyperparameters = HyperparameterJobsClient(api_key=api_key, logger=logger)
        self.models = ModelsClient(api_key=api_key, logger=logger)
        self.jobs = JobsClient(
            api_key=api_key,
            logger=logger,
            api_url=config.CONFIG_HOST,
        )
