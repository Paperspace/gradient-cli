import click
import six

from .config import config


class Logger(object):
    def _log(self, message, color=None, err=False):
        message = str(message)
        color = color if config.USE_CONSOLE_COLORS else None
        click.secho(message, fg=color, err=err)

    def log(self, message, color=None, err=False):
        self._log(message, color=color, err=err)

    def error(self, message):
        color = "red" if config.USE_CONSOLE_COLORS else None
        self._log(message, color=color, err=True)

    def warning(self, message):
        color = "yellow" if config.USE_CONSOLE_COLORS else None
        self._log(message, color=color)

    def log_error_response(self, data):
        messages = list(self._get_error_messages(data))
        msg = "\n".join(messages)

        if not msg:
            raise ValueError("No error messages found")

        self.error(msg)

    def _get_error_messages(self, data, add_prefix=False):
        if isinstance(data, dict):
            for key, value in sorted(data.items()):
                if key in ("error", "errors", "message", "messages"):
                    for message in self._get_error_messages(value):
                        yield message

                # when key == "details" and value is a dict then values should be prefixed with key
                if add_prefix:
                    for message in self._get_error_messages(value):
                        # there is some useless message in data["context"]
                        if key != "context":
                            yield key + ": " + message
                if key == "details":
                    for message in self._get_error_messages(value, add_prefix=True):
                        yield message

        if isinstance(data, list):
            for element in data:
                for message in self._get_error_messages(element):
                    yield message

        if isinstance(data, six.string_types):
            yield data

    def debug(self, message):
        if config.DEBUG:
            self._log("DEBUG: {}".format(message))

    def log_response(self, response, success_msg, error_msg):
        if response.ok:
            self._log(success_msg)
        else:
            try:
                data = response.json()
                self.log_error_response(data)
            except ValueError:
                self.error(error_msg)
