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
    def group(self, *args, **kwargs):
        aliases = []
        _args = args
        if args and isinstance(args[0], list):
            # we have a list so create group aliases
            aliases = args[0][1:]
            _args = [args[0][0]] + list(args[1:])

        if 'alias' in kwargs:
            aliases.append(kwargs.pop('alias'))

        def decorator(f):
            cmd = click.group(*_args, **kwargs)(f)
            self.add_command(cmd)
            for alias in set(aliases):
                alias_cmd = click.group(alias, **kwargs)(f)
                self.add_command(alias_cmd)
                alias_cmd.commands = cmd.commands
            return cmd

        return decorator


def prompt_for_secret(prompt):
    def callback_fun(ctx, param, value):
        if value is None:
            value = getpass.getpass(prompt)

        return value

    return callback_fun


def deprecated(version="1.0.0"):
    deprecated_invoke_notice = """DeprecatedWarning: \nWARNING: This command will not be included in version %s .
For more information, please see:

https://docs.paperspace.com
If you depend on functionality not listed there, please file an issue.""" % version

    def new_invoke(self, ctx):
        click.echo(click.style(deprecated_invoke_notice, fg='red'), err=True)
        super(type(self), self).invoke(ctx)

    def decorator(f):
        f.invoke = functools.partial(new_invoke, f)

    return decorator
