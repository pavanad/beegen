import git
from cleo.helpers import option

from beegen.commands.smart.base import SmartBaseCommand
from beegen.commands.smart.core.chain import load_chain


class SmartPullRequestDescriptionCommand(SmartBaseCommand):
    name = "smart pull-request-desc"
    description = (
        "Generate a pull request description based on "
        "commit messages from the active branch."
    )

    options = [
        option(
            long_name="language",
            short_name="l",
            description="Define the language for the description translation.",
            flag=False,
        )
    ]

    def handle(self) -> int:
        self.line("")

        if not self.check_provider():
            return

        language = self.option("language") or "English"
        self.line_prefix(
            f"Generating pull request description into <info>{language}</>."
        )

        try:
            with self.console.status("") as _:
                template = self.__get_template_pr()
                chain = load_chain(template, self.provider.chat_model)
                commit_messages = self.__get_git_commits()
                response = chain.invoke(
                    {"commit_messages": commit_messages, "language": language}
                )

            self.line_prefix("Pull Request Description:\n")
            self.print_markdown(f"```\n{response}\n```")
        except Exception:
            self.line_prefix(
                "<error>An error occurred while generating the description.</>"
            )
            self.line_prefix(
                "<error>Please ensure you are in a valid Git repository.</>\n"
            )

        self.line("")

    def __get_template_pr(self) -> str:
        return """
        Given the following commit messages, generate a detailed
        pull request description in {language}.

        Commit messages:
        {commit_messages}

        Pull request description:
        """

    def __get_git_commits(self) -> str:
        repo = git.Repo(search_parent_directories=True)
        branch = repo.active_branch.name
        commits = list(
            repo.iter_commits(branch, max_count=10, no_merges=True, first_parent=True)
        )
        commit_messages = [commit.message.strip() for commit in commits]
        return "\n".join(commit_messages)
