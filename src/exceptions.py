from http import HTTPStatus
from typing import Any, Dict, List, Type, Union, Optional

from fastapi.requests import Request
from fastapi.responses import UJSONResponse

from src.schemas.utils import NotFoundResponse


class UnicornException(Exception):
    def __init__(self,
                 status_code: int,
                 content: Optional[Union[str, Dict, List, Type[None]]] = None,
                 headers: Optional[Dict[str, Any]] = None):
        self.status_code = status_code
        self.content = content
        self.headers = headers


class NotFoundException(UnicornException):
    def __init__(self,
                 status_code: int = HTTPStatus.NOT_FOUND,
                 content: Optional[Union[str, Dict, List, Type[None]]] = None,
                 headers: Optional[Dict[str, Any]] = None):
        if not content:
            content = NotFoundResponse().dict()
        super().__init__(status_code, content, headers)


async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return UJSONResponse(
        status_code=exc.status_code,
        content=exc.content,
        headers=exc.headers
    )
