from uuid import UUID

from pydantic.dataclasses import dataclass

from app.shared.domain import Entity, ValueObject


@dataclass(eq=True, frozen=True)
class SchoolName(ValueObject):
    value: str


@dataclass
class School(Entity):
    id: UUID
    name: SchoolName
