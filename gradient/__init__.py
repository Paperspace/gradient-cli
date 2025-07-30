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

from gradient_utils import *

from .api_sdk import *
