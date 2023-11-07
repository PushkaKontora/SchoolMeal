from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Не найдено") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class LogicError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ValidationModelError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class UnprocessableEntity(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class BadRequest(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class AuthenticateError(HTTPException):
    def __init__(self, detail: str = "Ошибка аутентификации") -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class AuthorizationError(HTTPException):
    def __init__(self, detail: str = "Ошибка авторизации") -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    message = f"Ошибка валидации: {exc}"

    logger.error(request.url)
    logger.error(message)

    return JSONResponse(status_code=422, content={"detail": message})


async def default_handler(request: Request, exception: Exception) -> JSONResponse:
    logger.error(request.url)
    logger.error(exception)

    return JSONResponse(status_code=500, content={"detail": "Внутренняя ошибка сервера"})


async def logic_error_handler(request: Request, exception: LogicError) -> JSONResponse:
    logger.error(request.url)
    logger.error(exception.detail)

    return JSONResponse(status_code=exception.status_code, content={"detail": exception.detail})


async def validation_model_error_handler(request: Request, exception: ValidationModelError) -> JSONResponse:
    logger.error(request.url)
    logger.error(exception.detail)

    return JSONResponse(status_code=exception.status_code, content={"detail": exception.detail})


async def logging_http_error_handler(request: Request, exception: HTTPException) -> JSONResponse:
    logger.error(request.url)
    logger.error(exception.detail)

    return JSONResponse(status_code=exception.status_code, content={"detail": exception.detail})
