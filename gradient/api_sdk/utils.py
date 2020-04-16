import base64
import random
import string
from collections import OrderedDict

import six

from . import constants, sdk_exceptions


class MessageExtractor(object):
    def get_message_from_response_data(self, response_data, sep="\n"):
        """
        :type response_data: None|dict|list|str
        :type sep: str
        :rtype: str
        """
        messages = list(self.get_error_messages(response_data))
        msg = sep.join(messages)

        return msg

    def get_error_messages(self, data, add_prefix=False):
        if isinstance(data, dict):
            for key, value in sorted(data.items()):
                if key in ("error", "errors", "message", "messages", "title", "description"):
                    for message in self.get_error_messages(value):
                        yield message

                # when key == "details" and value is a dict then values should be prefixed with key
                if add_prefix:
                    for message in self.get_error_messages(value):
                        # there is some useless message in data["context"]
                        if key != "context":
                            yield key + ": " + message
                if key == "details":
                    for message in self.get_error_messages(value, add_prefix=True):
                        yield message

        if isinstance(data, list):
            for element in data:
                for message in self.get_error_messages(element):
                    yield message

        if isinstance(data, six.string_types):
            yield data


def print_dict_recursive(input_dict, logger, indent=0, tabulator="  "):
    for key, val in input_dict.items():
        logger.log("%s%s:" % (tabulator * indent, key))
        if type(val) is dict:
            print_dict_recursive(OrderedDict(val), logger, indent + 1)
        else:
            logger.log("%s%s" % (tabulator * (indent + 1), val))


class ExperimentsClientHelpersMixin(object):
    def _get_experiment_type_id(self, value):
        if isinstance(value, int):
            return value

        try:
            experiment_type_id = constants.MULTI_NODE_EXPERIMENT_TYPES_MAP[value]
        except KeyError as e:
            raise sdk_exceptions.GradientSdkError("Invalid experiment type: {}".format(e))

        return experiment_type_id


def validate_auth_options(auth_username, auth_password, generate_auth):
    if generate_auth and any((auth_username, auth_password)):
        raise sdk_exceptions.InvalidParametersError(
            "Use either auth_username and auth_password or generate_auth",
        )

    # checking if both or none auth parameters were used
    if len([val for val in (auth_username, auth_password) if not bool(val)]) == 1:
        raise sdk_exceptions.InvalidParametersError("auth_username and auth_password have to be used together")


def generate_credential(n):
    cred = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(n))
    return cred


def generate_credentials_pair(n):
    username = generate_credential(n)
    password = generate_credential(n)
    return username, password


def base64_encode(s):
    if six.PY3:
        s = bytes(s, encoding="utf8")

    encoded_str = base64.b64encode(s)

    if six.PY3:  # Python3's base64.b64encode returns a bytes instance so it should be converted back to unicode
        encoded_str = encoded_str.decode("utf-8")

    return encoded_str


def base64_encode_attribute(data, name):
    encoded_value = base64_encode(getattr(data, name))
    setattr(data, name, encoded_value)


def concatenate_urls(fst_part, snd_part):
    fst_part = fst_part if not fst_part.endswith("/") else fst_part[:-1]
    template = "{}{}" if snd_part.startswith("/") else "{}/{}"
    concatenated = template.format(fst_part, snd_part)
    return concatenated
