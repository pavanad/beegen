from configparser import ConfigParser

from beegen.config import settings

from .base import BaseCommand


class ConfigureCommand(BaseCommand):
    name = "configure"
    description = "Configure the LLM and access keys for usage."

    def handle(self) -> int:
        self.line("")

        provider = self.choice(
            f"{self.PREFIX}Please select your favorite LLM provider",
            ["Ollama", "OpenAI", "Google"],
            0,
        )
        model_name = self.ask_prefix("Model name:", "llama3")

        api_key = ""
        if provider != "Ollama":
            api_key = self.ask_prefix("API key:", "")

        self.line("")

        config = ConfigParser()
        config["foundation_model"] = {
            "provider": provider,
            "api_key": api_key,
            "model_name": model_name,
        }
        settings.set_configurations(config)
