from fastapi import HTTPException
from loguru import logger
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Не найдено") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class BadRequestError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UnprocessableEntityError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Ошибка аутентификации") -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class AuthorizationError(HTTPException):
    def __init__(self, detail: str = "Ошибка авторизации") -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


async def default_handler(request: Request, exception: Exception) -> JSONResponse:
    logger.error(request.url)
    logger.error(exception)

    return JSONResponse(status_code=500, content={"detail": "Внутренняя ошибка сервера"})
