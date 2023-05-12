from abc import ABC, abstractmethod

from fastapi import Request
from starlette.responses import JSONResponse

from app.responses import ErrorDescription, ErrorResponse


class Error(Exception, ABC):
    @property
    @abstractmethod
    def message(self) -> str:
        raise NotImplementedError

    @property
    def status_code(self) -> int:
        return 400


def handle_api_error(request: Request, exc: Error) -> JSONResponse:
    return JSONResponse(
        content=ErrorResponse(error=ErrorDescription(code=exc.__class__.__name__, msg=exc.message)).dict(),
        status_code=exc.status_code,
    )
