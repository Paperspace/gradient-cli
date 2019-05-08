from gradient_statsd import Client as StatsdClient

from .config import config
from .login import login, logout
from .utils import print_json_pretty
from .cli.cli import cli as _cli_entry_point

_ = StatsdClient  # to keep import safe from "Optimize Imports", auto code cleanup, etc.


def main():
    _cli_entry_point()
