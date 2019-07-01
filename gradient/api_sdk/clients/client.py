from .experiment_client import ExperimentsClient
from ..logger import MuteLogger


class SdkClient(object):
    def __init__(self, api_key, logger=MuteLogger()):
        """

        :type api_key: str
        :type logger: Logger
        """
        self.experiments = ExperimentsClient(api_key, logger)
