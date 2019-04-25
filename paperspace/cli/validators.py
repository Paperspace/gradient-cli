import re

import click


def validate_mutually_exclusive(options_1, options_2, error_message):
    used_option_in_options_1 = any(option is not None for option in options_1)
    used_option_in_options_2 = any(option is not None for option in options_2)
    if used_option_in_options_1 and used_option_in_options_2:
        raise click.UsageError(error_message)


def validate_email(ctx, param, value):
    if value is not None \
            and not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        raise click.BadParameter("Bad email address format")

    return value