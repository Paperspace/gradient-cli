from paperspace import logger


class CommandBase(object):
    def __init__(self, api=None, logger_=logger):
        self.api = api
        self.logger = logger_
