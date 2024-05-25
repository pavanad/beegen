from cleo.commands.command import Command
from pyfiglet import Figlet


class AboutCommand(Command):
    name = "about"
    description = "Shows information about BeeGen"

    def handle(self):
        custom_fig = Figlet(font="big")
        title = custom_fig.renderText("BeeGen")
        self.line(
            f"\n<fg=yellow>{title}</><fg=green>"
            "BeeGen is an intelligent command-line tool designed to assist developers\n"
            "with everyday tasks, leveraging the power of generative AI."
            "</>\n\n"
        )
