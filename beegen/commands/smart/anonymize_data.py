import os

from cleo.helpers import argument, option

from beegen.commands.smart.base import SmartBaseCommand
from beegen.commands.smart.core.chain import load_chain


class SmartAnonymizeCommand(SmartBaseCommand):
    name = "smart anonymize-data"
    description = (
        "Anonymize sensitive data with generative AI to "
        "ensure privacy by masking identifiable information."
    )

    arguments = [argument("text", "The text to anonymize.", optional=True)]
    options = [option("file", "f", description="Define text file", flag=False)]

    def handle(self) -> int:
        self.line("")
        self.line_prefix(
            "Loading model(LLM) from provider "
            f"<comment>{self.provider.provider_name}</>"
        )

        text = self.argument("text")
        text_file = self.option("file")

        if not any([text, text_file]):
            self.line_prefix("Please provide a text or a text file for anonymization")
            self.line("")
            return

        try:
            if text:

                with self.console.status("") as _:
                    response = self.__anonymize_text(text)

                if not response:
                    self.line_prefix(
                        "<error>An error occurred while anonymizing data.</>"
                    )
                    self.line_prefix(
                        "<info>Please change the model or try again later.</>\n\n"
                    )
                    return
                self.line_prefix("Anonymized text:\n")
                self.print_markdown(f"```\n{response}\n```")

            if text_file:
                text_file_path = os.path.abspath(text_file)
                text_file_content = self.__read_text_file(text_file_path)
                if text_file_content:
                    with self.console.status("") as _:
                        content = self.__anonymize_text(text_file_content)
                    filename = f"anonymized_{text_file}"
                    self.__save_text_file(filename, content)
                    self.line_prefix(f"Anonymized text saved to {filename}")

            self.line("")

        except Exception:
            self.line_prefix("<error>An error occurred while anonymizing data.</>")

    def __anonymize_text(self, text: str) -> str:
        template = self.__get_template_anonymize()
        chain = load_chain(template, self.provider.chat_model)
        return chain.invoke({"text": text})

    def __read_text_file(self, file_path: str) -> str:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        self.line_prefix("<error>Text file not found</>")
        return ""

    def __save_text_file(self, filename: str, content: str) -> bool:
        text_file_path = os.path.abspath(filename)
        with open(text_file_path, "w", encoding="utf-8") as file:
            file.write(content)

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
