from starlette.requests import Request
from starlette.responses import JSONResponse

from app.common.gateway.dto import ErrorModel
from app.common.gateway.errors import Error


response_400 = {400: {"model": ErrorModel}}
response_401 = {401: {"model": ErrorModel}}
response_404 = {404: {"model": ErrorModel}}
response_422 = {422: {"model": ErrorModel}}


def handle_error(request: Request, error: Error) -> JSONResponse:
    model = ErrorModel(error=error.__class__.__name__, message=error.message)

    return JSONResponse(content=model.dict(), status_code=error.status_code)
