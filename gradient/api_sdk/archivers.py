import fnmatch
import os
import zipfile

import progressbar

from .logger import MuteLogger


class ZipArchiver(object):
    DEFAULT_EXCLUDED_PATHS = [
        os.path.join(".git", "*"),
        os.path.join(".idea", "*"),
        os.path.join(".pytest_cache", "*"),
    ]

    def __init__(self, logger=None):
        self.logger = logger or MuteLogger()
        self.default_excluded_paths = self.DEFAULT_EXCLUDED_PATHS[:]

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

            for filename in files:
                # Create the full filepath by using os module.
                if relative_path == '.':
                    file_path = filename
                else:
                    file_path = os.path.join(os.path.relpath(root, input_path), filename)

                if any(fnmatch.fnmatch(file_path, pattern) for pattern in excluded_paths):
                    continue

                if file_path not in excluded_paths:
                    file_paths[file_path] = os.path.join(root, filename)

        return file_paths

    def _archive(self, file_paths, output_file_path):
        """Create ZIP archive and add files to it

        :param dict[str,str] file_paths:
        :param str output_file_path:
        """
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


class ZipArchiverWithProgressbar(ZipArchiver):
    def _archive(self, file_paths, output_file_path):
        """Create ZIP archive and add files to it and show progress bar in terminal

        :param dict[str,str] file_paths:
        :param str output_file_path:
        """
        self.bar = progressbar.ProgressBar(max_value=len(file_paths))
        super(ZipArchiverWithProgressbar, self)._archive(file_paths, output_file_path)
        self.bar.finish()

    def _archive_iterate_callback(self, i):
        self.bar.update(i)
