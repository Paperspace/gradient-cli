from gradient_statsd import Client as StatsdClient

from .api_sdk import *

_ = StatsdClient  # to keep import safe from "Optimize Imports", auto code cleanup, etc.
