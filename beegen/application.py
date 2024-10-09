import os

from cleo.application import Application as BaseApplication

from .commands.about import AboutCommand
from .commands.configure import ConfigureCommand
from .commands.mock import MockCreateCommand, MockRunCommand
from .commands.smart import (
    SmartAnonymizeCommand,
    SmartCreateVectorStoreCommand,
    SmartReadmeCommand,
    SmartRegexCommand,
    SmartTranslateCommand,
)
from .commands.snippets import (
    SnippetsAddCommand,
    SnippetsListCommand,
    SnippetsRemoveCommand,
    SnippetsUseCommand,
)
from .commands.utils import UtilsChatCommand
from .config import settings

try:
    from beegen.__version__ import __version__
except ImportError:
    from __version__ import __version__


class Application(BaseApplication):
    def __init__(self):
        super(Application, self).__init__("beegen", __version__)

        # create case not exists
        if not settings.config_path_exists():
            os.mkdir(settings.CONFIG_ROOT_PATH)

        # add commands
        for command in self.get_default_commands():
            self.add(command)

    def get_default_commands(self) -> list:
        commands = [
            AboutCommand(),
            MockCreateCommand(),
            MockRunCommand(),
            SnippetsAddCommand(),
            SnippetsListCommand(),
            SnippetsRemoveCommand(),
            SnippetsUseCommand(),
            ConfigureCommand(),
            SmartAnonymizeCommand(),
            SmartRegexCommand(),
            SmartReadmeCommand(),
            SmartCreateVectorStoreCommand(),
            SmartTranslateCommand(),
            UtilsChatCommand(),
        ]
        return commands
