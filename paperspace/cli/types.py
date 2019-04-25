import json

import click


class ChoiceType(click.Choice):
    """Takes a string-keyed map and converts cli-provided parameter to corresponding value"""

    def __init__(self, type_map, case_sensitive=True):
        super(ChoiceType, self).__init__(tuple(type_map.keys()), case_sensitive=case_sensitive)
        self.type_map = type_map

    def convert(self, value, param, ctx):
        value = super(ChoiceType, self).convert(value, param, ctx).upper()
        return self.type_map[value]


class Number(click.ParamType):
    name = "number"

    def convert(self, value, param, ctx):
        try:
            number = int(value)
        except ValueError:
            try:
                number = float(value)
            except ValueError:
                self.fail('{} is not a valid number'.format(value), param, ctx)

        return number


def json_string(val):
    """Wraps json.loads so the cli help shows proper option's type name instead of 'LOADS'"""
    return json.loads(val)