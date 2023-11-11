from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field

from app.common.api.utils import camelize_snakecase


class FrontendModel(BaseModel):
    class Config:
        alias_generator = camelize_snakecase
        allow_population_by_field_name = True


class OKSchema(FrontendModel):
    detail: str = "Операция успешно завершена"


class HTTPError(BaseModel):
    detail: str = Field(example="Сообщение ошибки")


class RoleOut(str, Enum):
    PARENT = "parent"
    TEACHER = "teacher"
    MEAL_ORGANIZER = "meal_organizer"
    CANTEEN_STAFF = "canteen_staff"


class AuthorizedUserOut(BaseModel):
    id: UUID
    role: RoleOut
