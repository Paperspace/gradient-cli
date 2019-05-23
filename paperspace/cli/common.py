import getpass

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


class ClickGroup(DYMMixin, HelpColorsGroup):
    pass


def prompt_for_secret(prompt):
    def callback_fun(ctx, param, value):
        if value is None:
            value = getpass.getpass(prompt)

        return value

    return callback_fun
