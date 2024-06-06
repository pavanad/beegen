import os

from cleo.helpers import argument, option

from beegen.commands.smart.base import SmartBaseCommand
from beegen.commands.smart.core.chain import load_chain


class SmartReadmeCommand(SmartBaseCommand):
    name = "smart readme"
    description = "Automatically generate a detailed README file for your project."

    arguments = [argument("project_path", description="The path to the project")]

    options = [
        option(
            long_name="language",
            short_name="l",
            description="Define the language for generating a readme file.",
            flag=False,
        )
    ]

    def handle(self) -> int:
        self.line("")

        project_path = self.argument("project_path")
        if not os.path.exists(project_path):
            self.line_prefix(f"Project path <error>'{project_path}'</> does not exist.")

        self.line(
            "<comment>"
            "Please provide one or more files with information or project "
            "configurations to improve the context.</>"
        )
        self.line(
            "<comment>Write the file names separated by commas "
            "(if there is more than one).</>\n"
        )
        self.line_prefix(
            "Loading model(LLM) from provider "
            f"<comment>{self.provider.provider_name}</>"
        )
        language = self.option("language") or "English"
        project_files = self.ask_prefix("Project files:", "")
        if not project_files:
            self.line_prefix("<error>No project files provided.</>")
            if self.confirm(
                f"{self.PREFIX}Do you like to continue without project files?", False
            ):
                self.__generate_readme(project_path, {}, language)
                return

            self.line("")
            return

        self.line_prefix("Loading project files...")
        context_files = self.__get_context_files(project_path, project_files)
        self.__generate_readme(project_path, context_files, language)

    def __generate_readme(self, path: str, context_files: dict, language: str):
        try:
            self.line_prefix("Generating README...")
            with self.console.status("") as _:
                project_details = self.__load_project(path)
                template = self.__get_template_readme()
                chain = load_chain(template, self.provider.chat_model)
                readme_text = chain.invoke(
                    {
                        "project_details": project_details,
                        "language": language,
                        "context_files": context_files,
                    }
                )
                self.__save_readme(readme_text)
        except Exception:
            self.line_prefix("<error>An error occurred while generating the readme.</>")
        finally:
            self.line("")

    def __get_context_files(self, path: str, files: str) -> str:
        context_files = ""
        list_files = files.split(",")
        for item in list_files:
            item = item.strip()
            file_path = os.path.join(path, item)
            if not os.path.exists(file_path):
                self.line_prefix(
                    f"<error>Project file '{file_path}' does not exist.</>"
                )
                return ""
            context_files += f"File: {item}\n{self.__load_file(file_path)}"
        return context_files

    def __load_file(self, file_path: str) -> str:
        with open(file_path, "r") as file:
            content = file.read()
            return content

    def __load_project(self, project_path: str) -> str:
        details = ""
        for dirpath, _, filenames in os.walk(project_path):
            check = any(["./." in dirpath, "__pycache__" in dirpath])
            if check:
                continue
            details += f"\nDirectory: {dirpath}\nFiles:\n"
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if self.__is_text_file(filepath):
                    details += f"- {filepath}\n"

        return details

    def __is_text_file(self, file_path, encoding="utf-8"):
        try:
            with open(file_path, "rb") as file:
                bytes = file.read(1024)
                bytes.decode(encoding)
            return True
        except (UnicodeDecodeError, TypeError):
            return False

    def __get_template_readme(self) -> str:
        return """
        You are a software developer with years of experience and need to create a
        README with relevant information about the project in Markdown. I will provide
        the directory structure, project file names, the language to be used, and the
        content of some files with relevant information or configurations about the
        project.

        List of directories and files:
        {project_details}

        Language:
        {language}

        Project files:
        {context_files}

        Try to generate the following topics in the "README":
        - Place a message in italics stating that this README was generated with the
        BeeGen tool.
        - Write a brief introduction.
        - Place some badges with the identified technologies just below the
        introduction text (without a title).
        - Perhaps a table with the main features of the project based on the provided
        files and directories (do not include the folder and file structure as
        it may be too large).
        - Prerequisites or dependencies according to the technology and the
        analyzed files.
        - Perhaps a message for contribution.
        """

    def __save_readme(self, readme_text: str):
        filename = "README.md"
        if os.path.exists(filename):
            filename = "README_generated.md"

        with open(filename, "w") as file:
            file.write(readme_text)
