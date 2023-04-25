from abc import ABC, abstractmethod

from fastapi import Request
from starlette.responses import JSONResponse

from app.base_entity import BaseEntity


class ErrorDescription(BaseEntity):
    code: str
    msg: str


class ErrorResponse(BaseEntity):
    error: ErrorDescription


class APIException(Exception, ABC):
    @property
    @abstractmethod
    def message(self) -> str:
        raise NotImplementedError

    @property
    def status_code(self) -> int:
        return 400


def handle_api_exception(request: Request, exc: APIException) -> JSONResponse:
    return JSONResponse(
        content=ErrorResponse(error=ErrorDescription(code=exc.__class__.__name__, msg=exc.message)).dict(),
        status_code=exc.status_code,
    )
