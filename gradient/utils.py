import json
import os
import shutil
from collections import OrderedDict

import click
import requests
import six

from gradient import exceptions


def get_terminal_lines(fallback=48):
    if six.PY3:
        return shutil.get_terminal_size().lines

    return fallback


def print_json_pretty(res):
    print(json.dumps(res, indent=2, sort_keys=True))


def response_error_check(res):
    if ('error' not in res
        and 'status' in res
        and (res['status'] < 200 or res['status'] > 299)):
        res['error'] = True
    return res


def requests_exception_to_error_obj(e):
    return { 'error': True, 'message': str(e) }


def status_code_to_error_obj(status_code):
    message = 'unknown'
    if status_code in requests.status_codes._codes:
        message = requests.status_codes._codes[status_code][0]
    return { 'error': True, 'message': message, 'status': status_code }


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
                if key in ("error", "errors", "message", "messages"):
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

        raise exceptions.WrongPathError("Given path is neither local path, nor valid URL")

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


def validate_workspace_input(input_data):
    workspace_url = input_data.get('workspaceUrl')
    workspace_path = input_data.get('workspace')
    workspace_archive = input_data.get('workspaceArchive')

    if (workspace_archive and workspace_path) \
            or (workspace_archive and workspace_url) \
            or (workspace_path and workspace_url):
        raise click.UsageError("Use either:\n\t--workspace https://path.to/git/repository.git - to point repository URL"
                               "\n\t--workspace /path/to/local/directory - to point on project directory"
                               "\n\t--workspace /path/to/local/archive.zip - to point on project .zip archive"
                               "\n\t--workspace none - to use no workspace"
                               "\n or neither to use current directory")
