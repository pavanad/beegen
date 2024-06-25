from cleo.helpers import argument, option

from beegen.commands.smart.base import SmartBaseCommand
from beegen.commands.smart.core.chain import load_chain


class SmartTranslateCommand(SmartBaseCommand):
    name = "smart translate"
    description = "Translate a given text into the specified language."

    arguments = [argument("text", "The value to translate.")]

    options = [
        option(
            long_name="language",
            short_name="l",
            description="Set the language for text translation.",
            flag=False,
        )
    ]

    def handle(self) -> int:
        self.line("")

        text = self.argument("text")
        language = self.option("language") or "English"
        self.line_prefix(f"Translating text into <info>{language}</>.")

        try:
            with self.console.status("") as _:
                template = self.__get_template_translate()
                chain = load_chain(template, self.provider.chat_model)
                response = chain.invoke({"text": text, "language": language})

            self.line_prefix("Translation:\n")
            self.print_markdown(f"```\n{response}\n```")
        except Exception:
            self.line_prefix("<error>An error occurred while translating the text.</>")

        self.line("")

    def __get_template_translate(self) -> str:
        return """
        Translate the text into the language specified below:

        Text:
        {text}

        Language:
        {language}

        Reminder: Return only the translated text.
        """
