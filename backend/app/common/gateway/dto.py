from functools import partial

from pydantic import BaseModel, Field


DatetimeField = partial(Field, example="2023-04-19T21:58:30.912109")


def _camelize_snakecase(string: str) -> str:
    parts = string.split("_")

    return parts[0].lower() + "".join(part.title() for part in parts[1:]) if len(parts) > 1 else string


class FrontendModel(BaseModel):
    class Config:
        alias_generator = _camelize_snakecase
        allow_population_by_field_name = True


class OKModel(FrontendModel):
    message: str = "Операция успешно завершена"


class ErrorModel(FrontendModel):
    error: str
    message: str
