from uuid import UUID

from pydantic import BaseModel, Field

from app.shared.fastapi.utils import camelize_snakecase
from app.user_management.domain.user import Role


class FrontendModel(BaseModel):
    class Config:
        alias_generator = camelize_snakecase
        allow_population_by_field_name = True


class OKSchema(FrontendModel):
    detail: str = "Операция успешно завершена"


class HTTPError(BaseModel):
    detail: str = Field(example="Сообщение ошибки")


class AuthorizedUser(BaseModel):
    id: UUID
    role: Role
