import os
import tempfile
import zipfile
from collections import OrderedDict

import six

from gradient.api_sdk.logger import MuteLogger


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


class ZipArchiver(object):
    DEFAULT_EXCLUDED_PATHS = [".git", ".idea", ".pytest_cache"]

    def __init__(self, temp_dir=None, logger=MuteLogger()):
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self.logger = logger
        self.default_excluded_paths = self.DEFAULT_EXCLUDED_PATHS

    def archive(self, input_dir_path, output_file_path, overwrite_existing_archive=True, exclude=None):
        """

        :param str input_dir_path:
        :param str output_file_path:
        :param bool overwrite_existing_archive:
        :param list|tuple|None exclude:
        """
        excluded_paths = self.get_excluded_paths(exclude)

        file_paths = self.get_file_paths(input_dir_path, excluded_paths)

        if os.path.exists(output_file_path):
            if not overwrite_existing_archive:
                raise IOError("File already exists")

            self.logger.log('Removing existing archive')
            os.remove(output_file_path)

        self.logger.log('Creating zip archive: %s' % output_file_path)
        self._archive(file_paths, output_file_path)
        self.logger.log('Finished creating archive: %s' % output_file_path)

    def get_excluded_paths(self, exclude=None):
        """
        :param list|tuple|None exclude:
        :rtype: set
        """
        if exclude is None:
            exclude = []

        excluded_paths = set(self.default_excluded_paths)
        excluded_paths.update(exclude)
        return excluded_paths

    @staticmethod
    def get_file_paths(input_path, excluded_paths=None):
        """Get a dictionary of all files in input_dir excluding specified in excluded_paths

        :param str input_path:
        :param list|tuple|set|None excluded_paths:
        :return: dictionary with full paths as values as keys and relative paths
        :rtype: dict[str,str]
        """
        if excluded_paths is None:
            excluded_paths = []

        file_paths = {}

        # Read all directory, subdirectories and file lists
        for root, dirs, files in os.walk(input_path):
            relative_path = os.path.relpath(root, input_path)
            if relative_path in excluded_paths:
                continue

            for filename in files:
                # Create the full filepath by using os module.
                if relative_path == '.':
                    file_path = filename
                else:
                    file_path = os.path.join(os.path.relpath(root, input_path), filename)

                if file_path not in excluded_paths:
                    file_paths[file_path] = os.path.join(root, filename)

        return file_paths

    def _archive(self, file_paths, output_file_path):
        zip_file = zipfile.ZipFile(output_file_path, 'w')
        with zip_file:
            i = 0
            for relative_path, abspath in file_paths.items():
                i += 1
                self.logger.debug('Adding %s to archive' % relative_path)
                zip_file.write(abspath, arcname=relative_path)
                self._archive_iterate_callback(i)

    def _archive_iterate_callback(self, i):
        pass
