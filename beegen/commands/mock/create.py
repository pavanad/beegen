import yaml
from cleo.helpers import argument

from beegen.commands.base import BaseCommand


class CreateCommand(BaseCommand):
    name = "mock create"
    description = "Generate a mockfile to configure the mock API."

    arguments = [
        argument("filename", description="Define the mock filename", optional=True)
    ]

    def handle(self) -> int:
        self.line("")

        filename = "mockfile.yml"
        if self.argument("filename"):
            filename = self.argument("filename")

        self.__generate_mockfile(filename)

    def __generate_mockfile(self, filename):
        self.line_prefix("Generating mockfile...")

        mockfile = self.__get_mockfile()
        with open(filename, "w") as f:
            yaml.dump(mockfile, f)

        self.line_prefix(f"Mockfile <comment>{filename}</comment> generated!")
        self.line("")

    def __get_mockfile(self) -> dict:
        return {
            "version": "1.0",
            "name": "beegen",
            "host": "0.0.0.0",
            "port": 8000,
            "workers": 2,
            "description": "BeeGen API mockfile",
            "endpoints": [
                {
                    "method": "GET",
                    "path": "/users",
                    "response": {
                        "status": 200,
                        "body": [
                            {
                                "id": 1,
                                "name": "John Doe",
                                "email": "john.doe@example.com",
                            },
                            {
                                "id": 2,
                                "name": "Jane Doe",
                                "email": "jane.doe@example.com",
                            },
                        ],
                    },
                },
                {
                    "method": "POST",
                    "path": "/user",
                    "request": {
                        "body": {
                            "id": 3,
                            "name": "New User",
                            "email": "new.user@example.com",
                        }
                    },
                    "response": {"status": 201, "body": {"status": "created"}},
                },
            ],
        }
