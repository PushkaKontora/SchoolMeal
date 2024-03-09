import re
from dataclasses import dataclass

from app.shared.domain.school_class import ClassID
from app.structure.domain.teacher import TeacherID


@dataclass(frozen=True, eq=True)
class Literal:
    value: str

    _REGEX = re.compile(r"[А-ЯЁ]")

    def __post_init__(self) -> None:
        if not self._REGEX.fullmatch(self.value):
            raise ValueError("Буква класса должны быть заглавной кириллицей")


@dataclass(frozen=True, eq=True, order=True)
class Number:
    value: int

    def __post_init__(self) -> None:
        if not 1 <= self.value <= 11:
            raise ValueError("Цифра класса должна быть от 1 до 11")


@dataclass
class SchoolClass:
    id: ClassID
    teacher_id: TeacherID
    number: Number
    literal: Literal
