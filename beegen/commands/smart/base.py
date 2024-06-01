from beegen.commands.base import BaseCommand
from beegen.commands.smart.core.provider import Provider
from beegen.config import settings


class SmartBaseCommand(BaseCommand):
    def __init__(self) -> None:
        super().__init__()
        self.__config = settings.get_configurations()
        self.provider = self.__load_provider()

    def __load_provider(self) -> Provider:
        if self.__config.has_section("foundation_model"):
            provider_config = dict(self.__config["foundation_model"])
            return Provider(provider_config)
        return None
