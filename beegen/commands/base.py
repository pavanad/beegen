from cleo.commands.command import Command


class BaseCommand(Command):

    PREFIX = "> <fg=yellow>[beegen]</> "

    def line_prefix(self, text, style=None, verbosity=None):
        text = self.PREFIX + text if text else ""
        self.line(text)
