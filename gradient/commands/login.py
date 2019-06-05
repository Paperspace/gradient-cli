from gradient import login, logout
from gradient.commands.common import CommandBase
from gradient.login import apikey, set_apikey
from gradient.version import version


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
