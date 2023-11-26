from uuid import UUID

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from app.children.domain.school import School


@dataclass(eq=True, frozen=True)
class ClassLiteral:
    value: str


@dataclass(eq=True, frozen=True)
class ClassNumber:
    value: int


class SchoolClass(BaseModel):
    id: UUID
    school: School
    number: ClassNumber
    literal: ClassLiteral
