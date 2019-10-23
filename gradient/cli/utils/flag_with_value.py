"""https://stackoverflow.com/questions/40753999/python-click-make-option-value-optional"""

import click
from click_didyoumean import DYMMixin
from click_help_colors import HelpColorsMixin

from gradient.cli.common import GradientOption


class RegisterReaderOptionMixin(object):
    """ Mark this option as getting a _set option """
    register_reader = True


class RegisterWriterOptionMixin(object):
    """ Fix the help for the _set suffix """

    def get_help_record(self, ctx):
        help = super(RegisterWriterOptionMixin, self).get_help_record(ctx)
        return (help[0].replace('_set ', '='),) + help[1:]


class RegisterWriterCommandMixin(object):
    def parse_args(self, ctx, args):
        """ Translate any opt= to opt_set= as needed """
        options = [o for o in ctx.command.params
                   if getattr(o, 'register_reader', None)]
        prefixes = {p for p in sum([o.opts for o in options], [])
                    if p.startswith('--')}
        for i, a in enumerate(args):
            try:
                a = a.split('=')
            except AttributeError:
                continue  # skip the following if a is not a string

            if a[0] in prefixes and len(a) > 1:
                a[0] += '_set'
                args[i] = '='.join(a)

        return super(RegisterWriterCommandMixin, self).parse_args(ctx, args)


class GradientRegisterReaderOption(RegisterReaderOptionMixin, GradientOption):
    pass


class GradientRegisterWriterOption(RegisterWriterOptionMixin, GradientOption):
    pass


class GradientRegisterWriterCommand(DYMMixin, HelpColorsMixin, RegisterWriterCommandMixin, click.Command):
    pass
