from enum import IntEnum, unique
from uuid import UUID

from pydantic.dataclasses import dataclass

from app.nutrition.domain.pupil import Pupil
from app.shared.domain.abc import Entity, ValueObject


@unique
class SchoolClassType(IntEnum):
    PRIMARY = 0
    HIGH = 1

    @classmethod
    def from_number(cls, number: int) -> "SchoolClassType":
        if 1 <= number <= 4:
            return SchoolClassType.PRIMARY

        if 5 <= number <= 11:
            return SchoolClassType.HIGH

        raise ValueError("Невалидный номер класса", number)


@dataclass(frozen=True, eq=True)
class SchoolClassInitials(ValueObject):
    literal: str
    number: int

    def __post_init_post_parse__(self) -> None:
        if not "A" <= self.literal <= "Я":
            raise ValueError("Буква класса должны быть кириллицей")

        if not 1 <= self.number <= 11:
            raise ValueError("Цифра класса должны быть от 1 до 11")

    @property
    def school_class_type(self) -> SchoolClassType:
        return SchoolClassType.PRIMARY if 1 <= self.number <= 4 else SchoolClassType.HIGH


class SchoolClass(Entity):
    id: UUID
    initials: SchoolClassInitials
    pupils: list[Pupil]
