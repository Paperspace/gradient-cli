from gradient.config import config
from .. import logger as sdk_logger
from .. import workspace
from ..clients import http_client


class BaseClient(object):
    API_URL = config.CONFIG_EXPERIMENTS_HOST
    DEFAULT_WORKSPACE_HANDLER_CLS = workspace.S3WorkspaceHandler

    def __init__(self, api_key, logger=sdk_logger.MuteLogger(), workspace_handler_cls=DEFAULT_WORKSPACE_HANDLER_CLS):
        """

        :type api_key: str
        :type logger: sdk_logger.Logger
        """
        self.client = http_client.API(self.API_URL, api_key=api_key, logger=logger)
        self.logger = logger
        self.workspace_handler = workspace_handler_cls(self.client)
