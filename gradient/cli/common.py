import functools
import json
import re

import click
import termcolor
import yaml
from click.exceptions import Exit
from click_didyoumean import DYMMixin
from click_help_colors import HelpColorsGroup

from gradient.api_sdk.config import config
from gradient.cli import cli_types

OPTIONS_FILE_OPTION_NAME = "optionsFile"
OPTIONS_FILE_PARAMETER_NAME = "options_file"
OPTIONS_DUMP_FILE_OPTION_NAME = "createOptionsFile"


def del_if_value_is_none(dict_, del_all_falsy=False):
    """Remove all elements with value == None"""
    for key, val in list(dict_.items()):
        if val is None or (del_all_falsy and not val):
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


def get_option_name(options_strings):
    for opt in options_strings:
        if not opt.startswith("-"):
            return opt

        if opt.startswith("--"):
            return opt[2:]


class ReadValueFromConfigFile(click.Parameter):
    def handle_parse_result(self, ctx, opts, args):
        config_file = ctx.params.get(OPTIONS_FILE_PARAMETER_NAME)
        if config_file:
            with open(config_file) as f:
                config_data = yaml.load(f, Loader=yaml.FullLoader)
                option_name = get_option_name(self.opts)
                value = config_data.get(option_name)
                if value is not None:
                    if isinstance(value, dict):
                        value = json.dumps(value)

                    opts[self.name] = value

        return super(ReadValueFromConfigFile, self).handle_parse_result(
            ctx, opts, args)


class ColorExtrasInCommandHelpMixin(object):
    def get_help_record(self, *args, **kwargs):
        rv = super(ColorExtrasInCommandHelpMixin,
                   self).get_help_record(*args, **kwargs)

        if not config.USE_CONSOLE_COLORS:
            return rv

        try:
            help_str = rv[1]
        except (IndexError, TypeError):
            return rv

        if help_str:
            help_str = self._color_extras(help_str)
            rv = rv[0], help_str
        return rv

    def _color_extras(self, s):
        pattern = re.compile(r"^.*(\[.*\])$")
        found = re.findall(pattern, s)
        if found:
            extras_str = found[-1]
            coloured_extras_str = self._color_str(extras_str)
            s = s.replace(extras_str, coloured_extras_str)

        return s

    def _color_str(self, s):
        s = termcolor.colored(s, config.HELP_HEADERS_COLOR)
        return s


class GradientArgument(ColorExtrasInCommandHelpMixin, ReadValueFromConfigFile, click.Argument):
    pass


class GradientOption(ColorExtrasInCommandHelpMixin, ReadValueFromConfigFile, click.Option):
    pass


api_key_option = click.option(
    "--apiKey",
    "api_key",
    help="API key to use this time only",
    cls=GradientOption,
)


def generate_options_template(ctx, param, value):
    if not value:
        return value

    params = {}
    dataset_value_lists = {}  # Value lists by dataset object key
    for param in ctx.command.params:
        option_name = get_option_name(param.opts)
        if option_name in (OPTIONS_FILE_OPTION_NAME, OPTIONS_DUMP_FILE_OPTION_NAME):
            continue

        option_value = ctx.params.get(param.name) or param.default

        # Add any value lists for dataset options to a separate dict
        paramVars = vars(param)
        if option_name.startswith("dataset"):
            # Drop the "dataset" prefix from the *option name*
            # and use the rest as the dataset object key.
            object_key = option_name[len("dataset"):]
            # list_suffix = "_list"
            # if object_key.endswith(list_suffix):
            #    object_key = object_key[:len(object_key)-len(list_suffix)]
            object_key = object_key[0].lower() + object_key[1:]
            dataset_value_lists[object_key] = option_value
            continue

        if isinstance(param.type, cli_types.ChoiceType):
            for key, val in param.type.type_map.items():
                if val == option_value:
                    option_value = key

        params[option_name] = option_value

    # Transform dataset value lists into dataset objects
    if "uri" in dataset_value_lists:
        # For each URI, add another dataset object to the list
        # using values across all option value lists
        datasets = []
        for i in range(len(dataset_value_lists["uri"])):
            dataset = {}
            for object_key, value_list in dataset_value_lists.items():
                if i < len(value_list):
                    dataset[object_key] = value_list[i]

            # Add dataset object to list
            datasets.append(dataset)

        # Add dataset object array to params
        params["datasets"] = datasets

    with open(value, "w") as f:
        yaml.safe_dump(params, f, default_flow_style=False)

    raise Exit  # to stop execution without executing the command


def options_file(f):
    options = [
        click.option(
            "--" + OPTIONS_FILE_OPTION_NAME,
            OPTIONS_FILE_PARAMETER_NAME,
            help="Path to YAML file with predefined options",
            type=click.Path(exists=True, resolve_path=True)
        ),
        click.option(
            "--" + OPTIONS_DUMP_FILE_OPTION_NAME,
            callback=generate_options_template,
            expose_value=False,
            help="Generate template options file",
            type=click.Path(writable=True, resolve_path=True)
        )
    ]
    return functools.reduce(lambda x, opt: opt(x), reversed(options), f)
