import datetime
import functools
import json
import re

import click
import six
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
        if self.should_read_value_from_file(opts, args, config_file):
            with open(config_file) as f:
                config_data = yaml.load(f, Loader=yaml.FullLoader)
                option_name = get_option_name(self.opts)
                if (isinstance(self, GradientObjectListOption) and
                        self.object_list_name in config_data):
                    value_list = []
                    for object_list_item in config_data[self.object_list_name]:
                        value_list.append(object_list_item.get(self.object_key))

                    if value_list:
                        opts[self.name] = value_list
                else:
                    value = config_data.get(option_name)
                    if value is not None:
                        if isinstance(value, dict):
                            value = json.dumps(value)
                        elif self.multiple and isinstance(value, six.string_types):
                            value = (value,)
                        # yaml.load turns datetime strings into datetime instances so we turn it back to a string
                        elif isinstance(value, datetime.datetime):
                            value = value.strftime("%Y-%m-%dT%H:%M:%S")

                        opts[self.name] = value

        rv = super(ReadValueFromConfigFile, self).handle_parse_result(
            ctx, opts, args)
        return rv

    def should_read_value_from_file(self, opts, args, config_file):
        """
        :rtype: bool
        """
        raise NotImplementedError


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
    def should_read_value_from_file(self, opts, args, config_file):
        return opts.get(self.name) in (None, ()) and config_file


class GradientOption(ColorExtrasInCommandHelpMixin, ReadValueFromConfigFile, click.Option):
    def should_read_value_from_file(self, opts, args, config_file):
        return self.name not in opts and config_file


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
    objects_value_lists = {}  # Object list name -> object key -> list of values
    for param in ctx.command.params:
        option_name = get_option_name(param.opts)
        if option_name in (OPTIONS_FILE_OPTION_NAME, OPTIONS_DUMP_FILE_OPTION_NAME):
            continue

        option_value = ctx.params.get(param.name) or param.default

        # If this is an object list type option, add its value list to
        # the specific object list set of value lists.
        if isinstance(param, GradientObjectListOption):
            new_value_list = option_value if option_value is not None else []
            object_list_name = param.object_list_name
            value_lists = objects_value_lists.setdefault(object_list_name, {})
            value_lists[param.object_key] = new_value_list
            continue

        if isinstance(param.type, cli_types.ChoiceType):
            for key, val in param.type.type_map.items():
                if val == option_value:
                    option_value = key

        params[option_name] = option_value

    # Transform value lists into objects
    object_lists = {}
    for object_list_name, value_lists in objects_value_lists.items():
        # Find maximum length value list and assume it lines up
        # with other object list options
        object_list = object_lists.setdefault(object_list_name, [])

        num_items = max(len(value_list) for value_list in value_lists.values())

        for i in range(num_items):
            new_object = {}
            for object_key, value_list in value_lists.items():
                if i < len(value_list):
                    new_object[object_key] = value_list[i]
                else:
                    new_object[object_key] = None

            object_list.append(new_object)

    # Add all object lists to overall params
    # for all non-empty object lists
    for object_list_name, object_list in object_lists.items():
        if object_list:
            params[object_list_name] = object_list

    with open(value, "w") as f:
        yaml.safe_dump(params, f, default_flow_style=False)

    raise Exit  # to stop execution without executing the command


def options_file(f):
    options = [
        click.option(
            "--" + OPTIONS_FILE_OPTION_NAME,
            OPTIONS_FILE_PARAMETER_NAME,
            is_eager=True,
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


class GradientObjectListOption(GradientOption):
    def __init__(self, object_name, param_decls, **kwargs):
        super(GradientObjectListOption, self).__init__(param_decls, **kwargs)
        self.object_name = object_name
        self.object_list_name = self.object_name + "s"
        self.object_key = self._compose_object_key()

    # Get this option's object key for the objects in the object list
    def _compose_object_key(self):
        option_name = get_option_name(self.opts)
        if not option_name.startswith(self.object_name):
            return option_name

        object_key = option_name[len(self.object_name):]
        object_key = object_key[0].lower() + object_key[1:]
        return object_key


class GradientDatasetOption(GradientObjectListOption):
    def __init__(self, param_decls, **kwargs):
        super(GradientDatasetOption, self).__init__("dataset", param_decls, **kwargs)


def validate_comma_split_option(comma_option_value, option_value, raise_if_no_values=False):
    if raise_if_no_values and not any((comma_option_value, option_value)):
        raise click.UsageError("No tags provided")

    if comma_option_value or option_value:
        if option_value:
            option_value = list(option_value)
        else:
            option_value = list()
        if comma_option_value:
            comma_option_value = [s.strip() for s in comma_option_value.split(",")]
            option_value.extend(comma_option_value)

        tags = sorted(set(option_value))
        return tags
