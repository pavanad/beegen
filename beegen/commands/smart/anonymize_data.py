from cleo.helpers import argument

from beegen.commands.smart.base import SmartBaseCommand
from beegen.commands.smart.core.chain import load_chain


class SmartAnonymizeCommand(SmartBaseCommand):
    name = "smart anonymize-data"
    description = (
        "Anonymize sensitive data with generative AI to "
        "ensure privacy by masking identifiable information."
    )

    arguments = [argument("text", "The text to anonymize.")]

    def handle(self) -> int:
        self.line("")
        self.line_prefix(
            "Loading model(LLM) from provider "
            f"<comment>{self.provider.provider_name}</>"
        )

        text = self.argument("text")
        try:
            with self.console.status("") as _:
                template = self.__get_template_anonymize()
                chain = load_chain(template, self.provider.chat_model)
                response = chain.invoke({"text": text})

            self.line_prefix("Anonymized text:\n")
            self.print_markdown(f"```\n{response}\n```")
            self.line("")

        except Exception:
            self.line_prefix("<error>An error occurred while anonymizing data.</>")

    def __get_template_anonymize(self) -> str:
        return """
        You are a data anonymization expert. Your task is to anonymize sensitive data
        such as names, emails, phone numbers, CPF, API keys, passwords, secret keys,
        or any type of sensitive information in the following text.
        Replace them with a placeholder (e.g., *** or [REDACTED]) while keeping the
        rest of the text intact.

        Original text: {text}

        Anonymized text:

        Reminder: Return only the anonymized text without any explanation.
        """
