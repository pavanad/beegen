import os

from cleo.helpers import argument, option

from beegen.commands.smart.base import SmartBaseCommand
from beegen.commands.smart.core.chain import load_chain


class SmartTranslateCommand(SmartBaseCommand):
    name = "smart translate"
    description = "Translate a given text into the specified language."

    arguments = [argument("text", "The value to translate.", optional=True)]

    options = [
        option(
            long_name="language",
            short_name="l",
            description="Set the language for text translation.",
            flag=False,
        ),
        option(
            long_name="file",
            short_name="f",
            description="Translate a file instead of a text.",
            flag=False,
        ),
    ]

    def handle(self) -> int:
        self.line("")

        text = self.argument("text")
        file_path = self.option("file")
        if not any([text, file_path]):
            self.line_prefix("<error>Please provide a text or file to translate.</>\n")
            return

        language = self.option("language") or "English"
        self.line_prefix(f"Translating text into <comment>{language}</>.")

        try:
            with self.console.status("") as _:
                if text:
                    response = self.__translate_text(text, language)
                elif file_path:
                    response = self.__translate_file(file_path, language)

            if text:
                self.line_prefix("Translation:\n")
                self.print_markdown(f"```\n{response}\n```")
            elif file_path:
                self.line_prefix(response)

        except Exception:
            self.line_prefix("<error>An error occurred while translating the text.</>")

        self.line("")

    def __translate_text(self, text: str, language: str) -> str:
        template = self.__get_template_translate()
        chain = load_chain(template, self.provider.chat_model)
        response = chain.invoke({"text": text, "language": language})
        return response

    def __translate_file(self, file_path: str, language: str) -> str:
        if not os.path.exists(file_path):
            return "<error>File not found for translation.</>"

        with open(file_path, "r") as file:
            text = file.read()
            response = self.__translate_text(text, language)

        filename, _ = os.path.splitext(file_path)
        with open(f"{filename}.translated", "w") as file:
            file.write(response)

        return f"Translation saved to <comment>{filename}.translated</>."

    def __get_template_translate(self) -> str:
        return """
        Translate the text into the language specified below:

        Text:
        {text}

        Language:
        {language}

        Reminder: Return only the translated text.
        """
