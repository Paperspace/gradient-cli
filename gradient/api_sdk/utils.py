import base64
import os
import random
import string
from collections import OrderedDict

import progressbar
import six
from requests_toolbelt.multipart import encoder

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


class MultipartEncoder(object):
    def __init__(self, fields):
        mp_encoder = encoder.MultipartEncoder(fields=fields)
        self.monitor = encoder.MultipartEncoderMonitor(mp_encoder, callback=self._create_callback(mp_encoder))

    def get_monitor(self):
        return self.monitor

    @staticmethod
    def _create_callback(encoder_obj):
        pass


class MultipartEncoderWithProgressbar(MultipartEncoder):
    @staticmethod
    def _create_callback(encoder_obj):
        bar = progressbar.ProgressBar(max_value=encoder_obj.len)

        def callback(monitor):
            if monitor.bytes_read == bar.max_value:
                bar.finish()
            else:
                bar.update(monitor.bytes_read)

        return callback


class PathParser(object):
    LOCAL_DIR = 0
    LOCAL_FILE = 1
    GIT_URL = 2
    S3_URL = 3

    @classmethod
    def parse_path(cls, path):
        if cls.is_local_dir(path):
            return cls.LOCAL_DIR

        if cls.is_local_zip_file(path):
            return cls.LOCAL_FILE

        if cls.is_git_url(path):
            return cls.GIT_URL

        if cls.is_s3_url(path):
            return cls.S3_URL

        raise sdk_exceptions.WrongPathError("Given path is neither local path, nor valid URL")

    @staticmethod
    def is_local_dir(path):
        return os.path.exists(path) and os.path.isdir(path)

    @staticmethod
    def is_local_zip_file(path):
        return os.path.exists(path) and os.path.isfile(path) and path.endswith(".zip")

    @staticmethod
    def is_git_url(path):
        return not os.path.exists(path) and path.endswith(".git") or path.lower().startswith("git:")

    @staticmethod
    def is_s3_url(path):
        return not os.path.exists(path) and path.lower().startswith("s3:")
