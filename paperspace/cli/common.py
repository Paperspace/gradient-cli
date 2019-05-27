import getpass

import click
from click import group
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
            cmd = group(*_args, **kwargs)(f)
            self.add_command(cmd)
            for alias in set(aliases):
                alias_cmd = group(alias, **kwargs)(f)
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
