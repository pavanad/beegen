import json

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import APIKeyHeader
from pydantic import ValidationError, create_model


class MockService:

    def __init__(self, mockfile: dict):
        self.__app = FastAPI()
        self.__api_key = None
        self.__api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
        self.__mockfile = mockfile
        self.__create_service()

    def __create_service(self):

        if "authentication" in self.__mockfile:
            self.__api_key = self.__mockfile["authentication"].get("key", None)
            api_key_name = self.__mockfile["authentication"].get("name", "X-API-Key")
            self.__api_key_header = APIKeyHeader(name=api_key_name, auto_error=False)

        self.__app.title = self.__mockfile.get("name", "beegen")
        self.__app.description = self.__mockfile.get(
            "description", "BeeGen API mockfile"
        )
        self.__app.version = self.__mockfile.get("version", "0.1.0")

        for item in self.__mockfile.get("endpoints", []):
            self.__create_routes(item)

    def __create_routes(self, endpoint: dict):

        request_model = None
        if "request" in endpoint:
            request = endpoint.get("request", [])
            fields = {field["name"]: (field["type"], ...) for field in request}
            request_model = create_model("RequestModel", **fields)

        response = endpoint["response"].get("body", {})

        async def route(request: Request, key: str = Depends(self.__api_key_header)):
            check = all(
                [
                    access == "protected",
                    key != self.__api_key,
                    "authentication" in self.__mockfile,
                ]
            )
            if check:
                raise HTTPException(status_code=401, detail="Unauthorized")

            try:
                if request.method in ["POST", "PUT", "PATCH"]:
                    data = await request.json()
                    if request_model:
                        data = request_model(**data)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON body")
            except ValidationError as e:
                raise HTTPException(status_code=422, detail=e.errors())
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

            return response

        methods = {
            "GET": self.__app.get,
            "POST": self.__app.post,
            "PUT": self.__app.put,
            "PATCH": self.__app.patch,
            "DELETE": self.__app.delete,
        }

        path = endpoint.get("path")
        method = endpoint.get("method")
        status = endpoint["response"].get("status", 200)
        access = endpoint.get("access", "public")

        methods.get(method)(path, status_code=status)(route)

    def run(self):
        port = self.__mockfile.get("port", 8000)
        host = self.__mockfile.get("host", "0.0.0.0")
        uvicorn.run(self.__app, host=host, port=port)
