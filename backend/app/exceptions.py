from abc import ABC, abstractmethod

from fastapi import Request
from starlette.responses import JSONResponse

from app.entities import BaseEntity


class DomainExceptionHandler(ABC):
    def handle(self, request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(content=self.body.dict(), status_code=self.status_code)

    @property
    @abstractmethod
    def exception(self) -> type[Exception]:
        raise NotImplementedError

    @property
    @abstractmethod
    def message(self) -> str:
        raise NotImplementedError

    @property
    def status_code(self) -> int:
        return 400

    @property
    def body(self) -> "ErrorResponse":
        return ErrorResponse(error=ErrorBody(code=self.exception.__name__, msg=self.message))


class ErrorBody(BaseEntity):
    code: str
    msg: str


class ErrorResponse(BaseEntity):
    error: ErrorBody
