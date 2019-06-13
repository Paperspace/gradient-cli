import six

if six.PY2:
    import xmlrpclib
else:
    import xmlrpc.client as xmlrpclib

from distutils.version import StrictVersion

from gradient import logger
from gradient.version import version


class PackageNotFoundError(Exception):
    pass


class VersionChecker(object):
    def is_up_to_date(self, module_name, current_version):
        version_in_repository = self.get_version_from_repository(module_name)

        up_to_date = StrictVersion(current_version) >= StrictVersion(version_in_repository)
        return up_to_date, version_in_repository

    def get_version_from_repository(self, module_name, repository_url="http://pypi.python.org/pypi"):
        pypi = xmlrpclib.ServerProxy(repository_url)
        versions = pypi.package_releases(module_name)
        if not versions:
            raise PackageNotFoundError("Package {} not found".format(module_name))

        return versions[0]


def look_for_new_version():
    vc = VersionChecker()
    try:
        g = vc.is_up_to_date("gradient", version)
        up_to_date, version_from_repository = g
    except Exception as e:
        logger.debug(e)
        return

    if not up_to_date:
        msg = "Warning: this version of the Gradient CLI ({current_version}) is out of date. " \
              "Some functionality might not be supported until you upgrade. \n\n" \
              "Run `pip install -U gradient` to upgrade\n".format(current_version=version)
        logger.warning(msg)
