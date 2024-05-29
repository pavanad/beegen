import json
import os
import pathlib

import yaml
from cleo.helpers import argument
from jsonschema import validate

from beegen.commands.base import BaseCommand
from beegen.services.mock import MockService


class MockRunCommand(BaseCommand):
    name = "mock run"
    description = "Run the mock API server using the mockfile."

    arguments = [
        argument(
            "filename",
            "Path to the yaml file containing the mock API configurations.",
            optional=True,
        )
    ]

    def handle(self) -> int:
        self.line("")

        filename = "mockfile.yml"
        if self.argument("filename"):
            filename = self.argument("filename")

        if os.path.exists(filename) is False:
            self.line_prefix(f"Mockfile <error>{filename}</error> not found!")
            self.line_prefix("Please create a mockfile first.")
            self.line("")
            return

        schema = self.__read_schema()
        mockfile = self.__read_mockfile(filename)

        self.line_prefix("Validating mockfile...")
        validate(mockfile, schema)

        self.line_prefix("Starting mock API server...")
        self.line("")

        service = MockService(mockfile)
        service.run()

    def __read_mockfile(self, filename: str) -> dict:
        self.line_prefix("Reading mockfile...")

        with open(filename, "r") as f:
            mockfile = yaml.safe_load(f)

        self.line_prefix(f"Mockfile <comment>{filename}</comment> read!")

        return mockfile

    def __read_schema(self) -> dict:
        current_path = pathlib.Path(__file__).parent.resolve()
        filename = f"{current_path}/schema.json"

        with open(filename, "r") as f:
            schema = json.load(f)

        return schema
