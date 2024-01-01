from uuid import UUID

from pydantic.dataclasses import dataclass

from app.children.domain.school import School
from app.shared.domain import Entity, ValueObject


@dataclass(eq=True, frozen=True)
class ClassLiteral(ValueObject):
    value: str


@dataclass(eq=True, frozen=True)
class ClassNumber(ValueObject):
    value: int


@dataclass
class SchoolClass(Entity):
    id: UUID
    school: School
    number: ClassNumber
    literal: ClassLiteral
