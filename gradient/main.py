from gradient import version_checker
from gradient.cli.cli import cli as _cli_entry_point


def main():
    version_checker.GradientVersionChecker.look_for_new_version_with_timeout()
    _cli_entry_point()
