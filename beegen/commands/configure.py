from configparser import ConfigParser

from cleo.helpers import option

from beegen.config import settings

from .base import BaseCommand


class ConfigureCommand(BaseCommand):
    name = "configure"
    description = "Configure the LLM and access keys for usage."

    options = [
        option(
            long_name="show",
            short_name="s",
            description="Show the current configuration.",
            flag=True,
        )
    ]

    def handle(self) -> int:
        self.line("")

        show_config = self.option("show")
        if show_config:
            self.__show_config()
            return

        self.__save_config()

    def __show_config(self) -> None:
        config = settings.get_configurations()
        if config.has_section("foundation_model"):
            provider_config = dict(config["foundation_model"])
            self.line_prefix("Current configuration:\n")
            self.line_prefix(f"<question>Provider:</> {provider_config['provider']}")
            self.line_prefix(
                f"<question>Model name:</> {provider_config['model_name']}"
            )
            self.line_prefix(
                f"<question>Embeddings name:</> {provider_config['embeddings_name']}\n"
            )
            return

        self.line_prefix("<error>LLM provider configuration not found.</>")
        self.line("")

    def __save_config(self) -> None:
        provider = self.choice(
            f"{self.PREFIX}Please select your favorite LLM provider",
            ["Ollama", "OpenAI", "Google"],
            0,
        )

        self.line("")
        model_name = self.ask_prefix("Model name:", "llama3")
        embeddings_name = self.ask_prefix("Embeddings model name:", "mxbai-embed-large")

        api_key = ""
        if provider != "Ollama":
            api_key = self.ask_prefix("API key:", "")

        self.line("")
        config = ConfigParser()
        config["foundation_model"] = {
            "provider": provider,
            "api_key": api_key,
            "model_name": model_name,
            "embeddings_name": embeddings_name,
        }
        settings.set_configurations(config)
