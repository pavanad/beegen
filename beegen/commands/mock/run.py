from cleo.helpers import argument

from beegen.commands.base import BaseCommand


class RunCommand(BaseCommand):
    name = "mock run"
    description = "Run the mock API server using the mockfile."

    arguments = [
        argument(
            "mockfile", "Path to the yaml file containing the mock API configurations."
        )
    ]

    def handle(self) -> int:
        print("mock run")
