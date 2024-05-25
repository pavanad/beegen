import uvicorn
from fastapi import FastAPI, Request


class MockService:
    def __init__(self, mockfile: dict):
        self.app = FastAPI()
        self.mockfile = mockfile
        self.__create_service()

    def __create_service(self):
        for item in self.mockfile.get("endpoints", []):
            self.__create_routes(item)

    def __create_routes(self, endpoint: dict):
        response = endpoint["response"].get("body", {})

        async def route(request: Request):
            return response

        methods = {
            "GET": self.app.get,
            "POST": self.app.post,
            "PUT": self.app.put,
            "DELETE": self.app.delete,
        }

        path = endpoint.get("path")
        method = endpoint.get("method")
        status = endpoint["response"].get("status", 200)
        methods.get(method)(path, status_code=status)(route)

    def run(self):
        port = self.mockfile.get("port", 8000)
        host = self.mockfile.get("host", "0.0.0.0")
        uvicorn.run(self.app, host=host, port=port)
