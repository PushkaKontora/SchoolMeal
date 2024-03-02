from fastapi import HTTPException
from loguru import logger
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


class NotFound(HTTPException):
    def __init__(self, detail: str = "Не найдено") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class BadRequest(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UnprocessableEntity(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class Unauthorized(HTTPException):
    def __init__(self, detail: str = "Ошибка аутентификации") -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class Forbidden(HTTPException):
    def __init__(self, detail: str = "Ошибка авторизации") -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


async def default_handler(_: Request, exception: Exception) -> JSONResponse:
    logger.critical(exception)

    return JSONResponse(status_code=500, content={"detail": "Внутренняя ошибка сервера"})


async def unprocessable_entity_handler(_: Request, exception: UnprocessableEntity) -> JSONResponse:
    logger.error(exception)

    return JSONResponse(status_code=422, content={"detail": str(exception)})
