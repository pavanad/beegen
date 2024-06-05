import os
import shutil

from cleo.helpers import argument

from beegen.commands.snippets.base import SnippetsBaseCommand


class SnippetsUseCommand(SnippetsBaseCommand):
    name = "snippets use"
    description = "Use the specified snippet."

    arguments = [argument("name", description="Set the snippet name")]

    def handle(self) -> int:
        self.line("")
        name = self.argument("name")
        if self.exists_snippet(name):
            snippet = self.__get_snippet(name)
            if snippet.get("code"):
                self.line_prefix("Code:\n")
                code = f"```\n{snippet.get('code')}\n```"
                self.print_markdown(code)
            else:
                self.line_prefix(
                    "The snippet is of type file, please specify the output file."
                )
                filename = self.ask_prefix("Output file:", "snippet.out")
                self.__save_output_file(filename, snippet)
                self.line_prefix(f"Snippet saved to <info>{filename}</>")
        else:
            self.line_prefix(f"Snippet <error>{name}</> not found")
        self.line("")

    def __get_snippet(self, name: str) -> dict:
        snippets = self.load_snippets()
        return snippets["items"][name]

    def __save_output_file(self, filename: str, snippet: dict):
        snippet_file = os.path.join(self.snippets_files_path, snippet.get("file"))
        snippet_output = os.path.join(os.path.curdir, filename)
        shutil.copy(snippet_file, snippet_output)
