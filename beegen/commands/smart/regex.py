from cleo.helpers import argument, option
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence

from beegen.commands.smart.base import SmartBaseCommand


class SmartRegexCommand(SmartBaseCommand):
    name = "smart regex"
    description = "Generate a regular expression based on the provided value."

    arguments = [argument("value", "The value to generate a regex for.")]
    options = [
        option(
            "language",
            "l",
            "The programming language to generate the example for.",
            flag=False,
        )
    ]

    def handle(self) -> int:
        self.line("")
        self.line_prefix(
            "Loading model(LLM) from provider "
            f"<comment>{self.provider.provider_name}</>"
        )

        value = self.argument("value")
        language = self.option("language") or "No Generate example"
        self.line_prefix("Generating a regex based on the provided value...")

        try:
            with self.console.status("") as _:
                chain = self.__load_chain()
                response = chain.invoke({"value": value, "language": language})

            self.line_prefix("Model response:\n")
            self.print_markdown(response)
        except Exception as error:
            print(f"{error}")
            self.line_prefix("<error>An error occurred while generating the regex.</>")

        self.line("")

    def __load_chain(self) -> RunnableSequence:
        template = self.__get_template_regex()
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.provider.chat_model | StrOutputParser()
        return chain

    def __get_template_regex(self) -> str:
        return """
        Create a regex based on the value provided below.
        Just create the regex, but if the user specifies the programming language,
        provide a simple example of how to use the regex in the chosen language.

        Value:
        {value}

        Language:
        {language}

        Reminder: Return only the regex and, if the user requests, the example
        in the specified language without any comments.
        """
