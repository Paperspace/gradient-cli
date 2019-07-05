import functools
import getpass
import json

import click
from click_didyoumean import DYMMixin
from click_help_colors import HelpColorsGroup

api_key_option = click.option(
    "--apiKey",
    "api_key",
    help="API key to use this time only",
)


def del_if_value_is_none(dict_):
    """Remove all elements with value == None"""
    for key, val in list(dict_.items()):
        if val is None:
            del dict_[key]


def jsonify_dicts(dict_):
    json_fields = [
        "envVars",
        "nodeAttrs"
    ]
    for field in json_fields:
        if field in dict_:
            dict_[field] = json.dumps(dict_[field])


class ClickGroup(DYMMixin, HelpColorsGroup):
    pass


def deprecated(msg):
    deprecated_invoke_notice = msg + """\nFor more information, please see:

https://docs.paperspace.com
If you depend on functionality not listed there, please file an issue."""

    def new_invoke(self, ctx):
        click.echo(click.style(deprecated_invoke_notice, fg='red'), err=True)
        super(type(self), self).invoke(ctx)

    def decorator(f):
        f.invoke = functools.partial(new_invoke, f)

    return decorator
