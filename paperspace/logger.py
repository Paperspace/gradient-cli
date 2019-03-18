import click
from six import string_types

from .config import config


def log(*messages, **kwargs):
    error = kwargs.get("error", False)
    for message in messages:
        click.echo(message, err=error)


def log_error_response(data):
    error = data.get("error")
    details = data.get("details")

    if not any((error, details)):
        raise ValueError("No error messages found")

    if error:
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


def debug(*messages):
    if config.DEBUG:
        log(*messages)
