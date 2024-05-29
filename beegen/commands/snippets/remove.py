from cleo.helpers import argument

from beegen.commands.snippets.base import SnippetsBaseCommand


class SnippetsRemoveCommand(SnippetsBaseCommand):
    name = "snippets remove"
    description = "Remove a snippet by its name."

    arguments = [argument("name", description="Set the snippet name")]

    def handle(self) -> int:
        self.line("")
        name = self.argument("name")
        if self.exists_snippet(name):
            if self.confirm("Do you want to remove this snippet?"):
                self.line("")
                self.remove_snippet(name)
                self.line_prefix(f"Snippet <comment>{name}</> removed")
        else:
            self.line_prefix(f"Snippet <error>{name}</> not found")
        self.line("")
