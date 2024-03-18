from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field

from app.shared.specifications import Specification, TrueSpecification
from app.user_management.domain.user import Role


T = TypeVar("T")


class FrontendBody(BaseModel):
    class Config:
        @staticmethod
        def _format(string: str) -> str:
            parts = string.split("_")

            return parts[0].lower() + "".join(part.title() for part in parts[1:]) if len(parts) > 1 else string

        alias_generator = _format
        allow_population_by_field_name = True


class FrontendParams(BaseModel):
    pass


class OKSchema(FrontendBody):
    detail: str = "Операция успешно завершена"


class HTTPError(BaseModel):
    detail: str = Field(example="Сообщение ошибки")


class AuthorizedUser(BaseModel):
    id: UUID
    role: Role


class Filters(Generic[T], FrontendParams, ABC):
    def to_specification(self) -> Specification[T]:
        map_ = self._build_map()

        spec: Specification[T] = TrueSpecification[T]()

        for attr, value in self.dict().items():
            if value is None:
                continue

            spec &= map_[attr](value)

        return spec

    @abstractmethod
    def _build_map(self) -> dict[str, Callable[[Any], Specification[T]]]:
        raise NotImplementedError
