import os
import uuid

from cleo.helpers import argument, option

from beegen.commands.snippets.base import SnippetsBaseCommand


class SnippetsAddCommand(SnippetsBaseCommand):
    name = "snippets add"
    description = "Add a new code snippet."

    arguments = [argument("name", description="Define the snippet name", optional=True)]
    options = [
        option(
            "code",
            "c",
            description="Define snippet code",
            flag=False,
        ),
        option(
            "file",
            "f",
            description="Define snippet file",
            flag=False,
        ),
    ]

    def handle(self) -> int:
        self.line("")

        name = self.argument("name")
        if not name:
            name = self.ask_prefix("Snippet name:", f"snippet-{str(uuid.uuid4())[:4]}")

        description = self.ask_prefix(
            "Description:", "Description default of the snippet"
        )

        snippet_code = self.option("code")
        snippet_file = self.option("file")

        if not any([snippet_code, snippet_file]):
            snippet_code = self.ask_prefix("Snippet code:")

        if snippet_file:
            snippet_file_path = os.path.abspath(snippet_file)
            saved, snippet_file = self.save_snippet_file(snippet_file_path)
            if not saved:
                self.line_prefix(
                    "<error>Unable to save the file, check if the path is correct</>"
                )
                return

        snippet = {
            "description": description,
            "code": snippet_code,
            "file": snippet_file,
        }

        self.__add_snippet(name, snippet)
        self.line("")

    def __add_snippet(self, name: str, snippet: dict) -> None:
        snippets = self.load_snippets()

        if self.exists_snippet(name):
            self.remove_snippet(name)

        snippets["items"][name] = snippet
        self.save_snippets(snippets)
        self.line_prefix(f"Snippet <comment>{name}</> added")
