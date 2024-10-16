import os
import sys

from streamlit.web import cli as stcli

from beegen.commands.base import BaseCommand


class UtilsChatCommand(BaseCommand):
    name = "utils chat"
    description = "BeeGen's chat interface for any language model"

    def handle(self) -> int:
        self.line("")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        two_levels_up = os.path.dirname(os.path.dirname(current_dir))
        app_path = os.path.join(two_levels_up, "services", "chat", "app.py")

        sys.argv = [
            "streamlit",
            "run",
            app_path,
            "--theme.base",
            "dark",
            "--theme.primaryColor",
            "#dca927",
            "--theme.backgroundColor",
            "#080808",
            "--theme.secondaryBackgroundColor",
            "#161616",
            "--client.showSidebarNavigation",
            "false",
        ]
        sys.exit(stcli.main())
