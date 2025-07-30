# noinspection PyUnresolvedReferences
import warnings

# Issue deprecation warning when the library is imported
warnings.warn(
    "gradient-cli v2 is deprecated. v3 of this project will host the DigitalOcean Gradient SDK. "
    "Development for the new version will be in https://github.com/digitalocean/gradient-python. "
    "Users are advised to pin to v2 of this library.",
    DeprecationWarning,
    stacklevel=2,
)

# Redirect distutils to setuptools._distutils
# This is necessary to avoid issues with setuptools and distutils compatibility in python 3.12+
import sys
import types
import setuptools._distutils as _distutils

# Create a fake 'distutils' module pointing to setuptools._distutils
sys.modules["distutils"] = _distutils

# Also redirect submodules like distutils.core, distutils.version, etc.
sys.modules["distutils.core"] = _distutils.core
# sys.modules["distutils.version"] = _distutils.version
sys.modules["distutils.spawn"] = _distutils.spawn
# sys.modules["distutils.sysconfig"] = _distutils.sysconfig


from gradient_utils import *

from .api_sdk import *
