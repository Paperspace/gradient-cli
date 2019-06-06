import click
from six import string_types

from .config import config


def _log(message, color=None, err=False):
    message = str(message)
    color = color if config.USE_CONSOLE_COLORS else None
    click.secho(message, fg=color, err=err)


def log(message, color=None, err=False):
    _log(message, color=color, err=err)


def error(message):
    color = "red" if config.USE_CONSOLE_COLORS else None
    _log(message, color=color, err=True)


def warning(message):
    color = "yellow" if config.USE_CONSOLE_COLORS else None
    _log(message, color=color)


def log_error_response(data):
    error_str = data.get("error")
    details = data.get("details")
    message = data.get("message")

    if not any((error_str, details, message)):
        raise ValueError("No error messages found")

    if error_str:
        try:
            error(error_str["message"])
        except (KeyError, TypeError):
            error(str(error_str))

    if details:
        if isinstance(details, dict):
            for key, val in details.items():
                if isinstance(val, string_types):
                    val = [val]

                for v in val:
                    msg = "{}: {}".format(key, str(v))
                    error(msg)
        else:
            error(details)

    if message:
        error(str(message))


def debug(messages):
    if config.DEBUG:
        log("DEBUG: {}".format(messages))


def log_response(response, success_msg, error_msg):
    if response.ok:
        log(success_msg)
    else:
        try:
            data = response.json()
            log_error_response(data)
        except ValueError:
            error(error_msg)
