from dataclasses import dataclass
from typing import NewType
from uuid import UUID, uuid4

from app.nutrition.domain.mealtime import Mealtime
from app.shared.exceptions import DomainException


TeacherID = NewType("TeacherID", UUID)


@dataclass(frozen=True)
class ClassID:
    value: UUID

    @classmethod
    def generate(cls) -> "ClassID":
        return cls(uuid4())


@dataclass(frozen=True)
class Literal:
    value: str

    def __post_init__(self) -> None:
        if not "А" <= self.value <= "Я":
            raise DomainException("Буква класса должна быть кириллицей")


@dataclass(frozen=True)
class Number:
    value: int

    def __post_init__(self) -> None:
        if not 1 <= self.value <= 11:
            raise DomainException("Цифра класса должны быть от 1 до 11")


@dataclass
class SchoolClass:
    id: ClassID
    teacher_id: TeacherID | None
    number: Number
    literal: Literal
    mealtimes: set[Mealtime]
