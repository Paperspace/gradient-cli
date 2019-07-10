from gradient.config import config
from .. import logger as sdk_logger
from .. import workspace
from ..clients import http_client


class BaseClient(object):
    DEFAULT_WORKSPACE_HANDLER_CLS = workspace.S3WorkspaceHandler

    def __init__(
            self, api_key,
            logger=sdk_logger.MuteLogger(),
            api_url=config.CONFIG_EXPERIMENTS_HOST,
            workspace_handler_cls=DEFAULT_WORKSPACE_HANDLER_CLS
    ):
        """

        :param str api_key:
        :param sdk_logger.Logger logger:
        :param str api_url:
        :param type[workspace.WorkspaceHandler] workspace_handler_cls:
        """
        self.api_key = api_key
        self.api_url = api_url
        self.client = http_client.API(self.api_url, api_key=api_key, logger=logger)
        self.logger = logger
        self.workspace_handler = workspace_handler_cls(experiments_api=self.client)
