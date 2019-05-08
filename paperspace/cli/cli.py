import click

from paperspace import config
from paperspace.cli import common
from paperspace.commands import login as login_commands


@click.group(cls=common.ClickGroup, **config.HELP_COLORS_DICT)
def cli():
    pass


# TODO: delete experiment - not implemented in the api
# TODO: modify experiment - not implemented in the api
# TODO: create experiment template?? What is the difference between experiment and experiment template?


@cli.command("version", help="Show the version and exit")
def version():
    command = login_commands.ShowVersionCommand()
    command.execute()


if __name__ == '__main__':
    cli()
