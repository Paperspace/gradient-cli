import click
from six import string_types

from .config import config


def log(message, **kwargs):
    error = kwargs.get("error", False)
    click.echo(message, err=error)


def log_error_response(data):
    error = data.get("error")
    details = data.get("details")
    message = data.get("message")

    if not any((error, details, message)):
        raise ValueError("No error messages found")

    if error:
        try:
            log(error["message"], error=True)
        except (KeyError, TypeError):
            log(str(error), error=True)

    if details:
        if isinstance(details, dict):
            for key, val in details.items():
                if isinstance(val, string_types):
                    val = [val]

                for v in val:
                    msg = "{}: {}".format(key, str(v))
                    log(msg, error=True)
        else:
            log(details)

    if message:
        log(str(message), error=True)


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
            log(error_msg)
