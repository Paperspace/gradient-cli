import os
import sys
from platform import system
import json

import requests
from distutils.version import StrictVersion

from gradient.clilogger import CliLogger
from gradient.version import version

logger = CliLogger()


class PackageNotFoundError(Exception):
    pass


class VersionChecker(object):
    def is_up_to_date(self, module_name, current_version):
        version_in_repository = self.get_version_from_repository(module_name)

        up_to_date = StrictVersion(current_version) >= StrictVersion(
            version_in_repository
        )
        return up_to_date, version_in_repository

    def get_version_from_repository(
        self, module_name, repository_url="https://pypi.org/pypi"
    ):
        # Use PyPI JSON API instead of XML-RPC
        json_url = f"{repository_url}/{module_name}/json"

        try:
            response = requests.get(json_url, timeout=5)
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, json.JSONDecodeError) as e:
            raise PackageNotFoundError(
                "Package {} not found or API error: {}".format(module_name, str(e))
            )

        # Get all release versions
        releases = data.get("releases", {})
        if not releases:
            raise PackageNotFoundError(
                "No releases found for package {}".format(module_name)
            )

        # Get all version numbers
        versions = list(releases.keys())
        if not versions:
            raise PackageNotFoundError(
                "No versions found for package {}".format(module_name)
            )

        # Filter to only include versions < 3.0 (v2 versions only)
        v2_versions = []
        for v in versions:
            try:
                if StrictVersion(v) < StrictVersion("3.0.0"):
                    v2_versions.append(v)
            except ValueError:
                # Skip invalid version strings
                continue

        if not v2_versions:
            # If no v2 versions found, raise exception to skip the check
            raise PackageNotFoundError(
                "No v2 versions found for package {}".format(module_name)
            )

        # Sort v2_versions to get the latest one (highest version number)
        v2_versions.sort(key=lambda x: StrictVersion(x), reverse=True)
        return v2_versions[0]


class GradientVersionChecker(object):
    @classmethod
    def look_for_new_version_with_timeout(cls):
        if not cls._should_check_version():
            return

        if not system() == "Linux":
            cls.look_for_new_version()
            return

        import signal

        class TimeoutError(Exception):
            pass

        def handler(signum, frame):
            raise TimeoutError

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(1)

        try:
            cls.look_for_new_version()
        except TimeoutError:
            pass

        signal.alarm(0)

    @staticmethod
    def look_for_new_version():
        vc = VersionChecker()
        try:
            up_to_date, version_from_repository = vc.is_up_to_date("gradient", version)
        except Exception as e:
            logger.debug(e)
            return

        if not up_to_date:
            msg = (
                "Warning: this version of the Gradient CLI ({current_version}) is out of date. "
                "Some functionality might not be supported until you upgrade. \n\n"
                "The latest v2 version is {version_from_repository}.\n"
                'Run `pip install -U "gradient<3.0"` to upgrade to the latest v2 version\n'
                "Note: v3+ will be the DigitalOcean Gradient SDK. Pin to v2 to avoid breaking changes.\n".format(
                    current_version=version
                )
            )
            logger.warning(msg)

    @staticmethod
    def _should_check_version():
        if not hasattr(sys.stdin, "isatty"):
            return False
        if not sys.stdin.isatty() or not sys.stdout.isatty():
            return False
        if os.getenv("PAPERSPACE_CLI_DEV") == "true":
            return False

        return True
