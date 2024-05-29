import secrets

import yaml
from cleo.helpers import argument

from beegen.commands.base import BaseCommand


class MockCreateCommand(BaseCommand):
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
            "version": "0.1.0",
            "name": "BeeGen API",
            "host": "0.0.0.0",
            "port": 8000,
            "description": "BeeGen mockfile API example",
            "authentication": {
                "type": "api_key",
                "key": secrets.token_urlsafe(32),
                "name": "X-API-Key",
            },
            "endpoints": [
                {
                    "method": "GET",
                    "path": "/users",
                    "access": "public",
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
                    "access": "protected",
                    "request": [
                        {
                            "name": "id",
                            "type": "int",
                            "description": "The user ID",
                        },
                        {
                            "name": "name",
                            "type": "str",
                            "description": "The user name",
                        },
                        {
                            "name": "email",
                            "type": "str",
                            "description": "The user email",
                        },
                    ],
                    "response": {"status": 201, "body": {"status": "created"}},
                },
            ],
        }
