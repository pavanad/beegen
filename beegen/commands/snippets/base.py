import json
import os
import shutil
import uuid
from typing import Tuple

from beegen.commands.base import BaseCommand
from beegen.config import settings


class SnippetsBaseCommand(BaseCommand):
    snippets_path = os.path.join(settings.CONFIG_ROOT_PATH, "snippets")
    snippets_filename = os.path.join(snippets_path, "snippets.json")
    snippets_files_path = os.path.join(snippets_path, "files")

    def __init__(self):
        super().__init__()
        if not os.path.exists(self.snippets_path):
            os.mkdir(self.snippets_path)
            os.mkdir(self.snippets_files_path)

    def load_snippets(self) -> list:
        """Load snippets from a JSON file."""
        snippets = {"items": {}}
        if os.path.exists(self.snippets_filename):
            try:
                with open(self.snippets_filename, "r", encoding="utf-8") as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError) as e:
                self.line_prefix(f"<error>Error loading snippets: {e}</>")
        return snippets

    def save_snippets(self, snippets: list) -> None:
        """Save snippets to a JSON file."""
        try:
            with open(self.snippets_filename, "w", encoding="utf-8") as file:
                json.dump(snippets, file, ensure_ascii=False, indent=4)
        except IOError as e:
            self.line_prefix(f"<error>Error saving snippets: {e}</>")

    def save_snippet_file(self, filename: str) -> Tuple[bool, str]:
        """Save snippet file."""
        if os.path.exists(filename):
            dest_filename = f"snippet-file-{str(uuid.uuid4())[:4]}.snippet"
            new_snippet_filename = os.path.join(self.snippets_files_path, dest_filename)
            shutil.copy(filename, new_snippet_filename)
            return True, dest_filename

        self.line_prefix("<error>Snippet file not found</>")
        return False

    def remove_snippet(self, name: str) -> None:
        """Remove snippet."""
        snippets = self.load_snippets()
        items = snippets["items"]

        if items[name].get("file"):
            snippet_file = os.path.join(self.snippets_files_path, items[name]["file"])
            os.remove(snippet_file)

        del snippets["items"][name]
        self.save_snippets(snippets)

    def exists_snippet(self, name: str) -> bool:
        """Check if snippet exists."""
        snippets = self.load_snippets()
        return name in snippets["items"]
