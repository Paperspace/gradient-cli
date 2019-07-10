from gradient.config import config
from .deployment_client import DeploymentsClient
from .experiment_client import ExperimentsClient
from .job_client import JobsClient
from .. import logger as sdk_logger
from ..workspace import WorkspaceHandler


class SdkClient(object):
    def __init__(self, api_key, logger=sdk_logger.MuteLogger()):
        """

        :type api_key: str
        :type logger: sdk_logger.Logger
        """
        self.experiments = ExperimentsClient(api_key=api_key, logger=logger)
        self.deployments = DeploymentsClient(api_key=api_key, logger=logger, api_url=config.CONFIG_HOST)
        self.jobs = JobsClient(
            api_key=api_key,
            logger=logger,
            api_url=config.CONFIG_HOST,
            workspace_handler_cls=WorkspaceHandler
        )
