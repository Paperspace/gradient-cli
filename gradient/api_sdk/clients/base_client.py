from .. import logger as sdk_logger


class BaseClient(object):
    def __init__(
            self, api_key,
            logger=sdk_logger.MuteLogger()
    ):
        """
        Base class. All client classes inherit from it.

        An API key can be created at paperspace.com after you sign in to your account. After obtaining it, you can set
        it in the CLI using the command::

            gradient apiKey XXXXXXXXXXXXXXXXXXX

        or you can provide your API key in any command, for example::

            gradient experiments run ... --apiKey XXXXXXXXXXXXXXXXXXX

        :param str api_key: your API key
        :param sdk_logger.Logger logger:
        """
        self.api_key = api_key
        self.logger = logger
