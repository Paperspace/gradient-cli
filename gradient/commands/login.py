from gradient import clilogger
from gradient.login import login, logout
from gradient.login import set_apikey
from gradient.version import version


class CommandBase(object):
    def __init__(self, api=None, logger_=clilogger.CliLogger()):
        self.api = api
        self.logger = logger_


class LogInCommand(CommandBase):
    def execute(self, email, password, api_token_name=None):
        login(email, password, api_token_name)


class LogOutCommand(CommandBase):
    def execute(self):
        logout()


class ShowVersionCommand(CommandBase):
    def execute(self):
        self.logger.log(version)


class SetApiKeyCommand(CommandBase):
    def execute(self, api_key):
        if not api_key:
            self.logger.error("API Key cannot be empty.")
            return

        set_apikey(api_key)
