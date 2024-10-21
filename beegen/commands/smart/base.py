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
            try:
                provider_config = dict(self.__config["foundation_model"])
                return Provider(provider_config)
            except Exception:
                pass
        return None

    def check_provider(self) -> bool:
        if self.provider is None:
            self.line_prefix("<error>LLM provider configuration not found.</>")
            self.line_prefix(
                "Please run the command below to set up the required settings:\n"
            )
            self.print_markdown("```\nbeegen configure\n```")
            self.line("")

            self.line_prefix("You may also want to check your current configuration:\n")
            self.print_markdown("```\nbeegen configure --show\n```")
            self.line("")

            return False
        return True
