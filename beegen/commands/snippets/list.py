from beegen.commands.snippets.base import SnippetsBaseCommand


class SnippetsListCommand(SnippetsBaseCommand):
    name = "snippets list"
    description = "List all available snippets."

    def handle(self) -> int:
        self.line("")

        snippets = self.load_snippets()
        if not snippets.get("items"):
            self.line_prefix("No snippets found.")
            self.line("")
            return

        table = self.table()
        table.set_headers(["Snippet", "Description", "Type"])
        table.set_rows(
            [
                [
                    item,
                    value.get("description"),
                    "Code" if value.get("code") else "File",
                ]
                for item, value in snippets.get("items", {}).items()
            ]
        )
        table.render()
        self.line("")
