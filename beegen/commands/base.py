from typing import Any

from cleo.commands.command import Command
from rich.console import Console
from rich.markdown import Markdown


class BaseCommand(Command):

    PREFIX = "> <fg=yellow>[beegen]</> "

    def __init__(self) -> None:
        super().__init__()
        self.console = Console()

    def line_prefix(self, text, style=None, verbosity=None):
        text = self.PREFIX + text if text else ""
        self.line(text)

    def ask_prefix(self, question: str, default: Any) -> Any:
        question = self.PREFIX + question if question else ""
        self.ask(question, default)

    def print_markdown(self, text: str):
        markdown = Markdown(text)
        self.console.print(markdown)
