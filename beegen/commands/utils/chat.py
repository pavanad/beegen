import os
import subprocess

from beegen.commands.base import BaseCommand


class UtilsChatCommand(BaseCommand):
    name = "utils chat"
    description = "BeeGen's chat interface for any language model"

    def handle(self) -> int:
        self.line("")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        two_levels_up = os.path.dirname(os.path.dirname(current_dir))

        app_path = os.path.join(two_levels_up, "services", "chat", "app.py")
        subprocess.run(["streamlit", "run", app_path])
