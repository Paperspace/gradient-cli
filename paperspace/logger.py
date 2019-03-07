import click
from six import string_types


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
        for key, val in details.items():
            if isinstance(val, string_types):
                val = [val]

            for v in val:
                msg = "{}: {}".format(key, str(v))
                log(msg, error=True)
