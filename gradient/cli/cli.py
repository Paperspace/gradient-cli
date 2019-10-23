import click
import click_completion

from gradient.api_sdk.config import config
from gradient.api_sdk.sdk_exceptions import GradientSdkError
from gradient.cli import common
from gradient.commands import login as login_commands
from gradient.exceptions import ApplicationError
from gradient.logger import Logger

click_completion.init()


class GradientGroup(common.ClickGroup):
    def main(self, *args, **kwargs):
        try:
            super(GradientGroup, self).main(*args, **kwargs)
        except (ApplicationError, GradientSdkError) as e:
            if config.DEBUG:
                raise

            Logger().error(e)


@click.group(cls=GradientGroup, **config.HELP_COLORS_DICT)
def cli():
    pass


# TODO: delete experiment - not implemented in the api
# TODO: modify experiment - not implemented in the api
# TODO: create experiment template?? What is the difference between experiment and experiment template?


@cli.command("version", help="Show the version and exit")
def get_version():
    command = login_commands.ShowVersionCommand()
    command.execute()


if __name__ == '__main__':
    cli()
