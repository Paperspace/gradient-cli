from click import secho

from gradient.api_sdk.utils import MessageExtractor
from .config import config


class Logger(object):
    def _log(self, message, color=None, err=False):
        message = str(message)
        color = color if config.USE_CONSOLE_COLORS else None
        secho(message, fg=color, err=err)

    def log(self, message, color=None, err=False):
        self._log(message, color=color, err=err)

    def error(self, message):
        color = "red" if config.USE_CONSOLE_COLORS else None
        self._log(message, color=color, err=True)

    def warning(self, message):
        color = "yellow" if config.USE_CONSOLE_COLORS else None
        self._log(message, color=color)

    def log_error_response(self, data):
        msg = MessageExtractor().get_message_from_response_data(data)
        if not msg:
            raise ValueError("No error messages found")

        self.error(msg)

    def debug(self, message):
        if config.DEBUG:
            self._log("DEBUG: {}".format(message))

    def log_response(self, response, success_msg, error_msg):
        """
        :type response: requests.Response|http_client.GradientResponse
        :type success_msg: str
        :type error_msg: str
        """
        if response.ok:
            self._log(success_msg)
        else:
            try:
                data = response.json()
                self.log_error_response(data)
            except ValueError:
                self.error(error_msg)
            except AttributeError:
                if response.data:
                    self.log_error_response(response.data)
                else:
                    self.error(response)
