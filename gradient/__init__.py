import platform

from gradient_statsd import Client as StatsdClient

from .config import config
from .login import login, logout
from .utils import print_json_pretty
from .cli.cli import cli as _cli_entry_point
from .version_checker import look_for_new_version

_ = StatsdClient  # to keep import safe from "Optimize Imports", auto code cleanup, etc.


def _look_for_new_version_with_timeout():
    if not platform.system() == "Linux":
        look_for_new_version()
        return

    import signal

    class TimeoutError(Exception):
        pass

    def handler(signum, frame):
        raise TimeoutError

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(1)

    try:
        look_for_new_version()
    except TimeoutError:
        pass

    signal.alarm(0)


def main():
    _look_for_new_version_with_timeout()
    _cli_entry_point()

