from enum import Enum, unique
from typing import Any, Callable
from uuid import UUID

from pydantic import BaseModel

from app.shared.api.dto import Filters
from app.shared.domain.personal_info import FullName
from app.shared.domain.pupil import PupilID
from app.shared.domain.school_class import ClassID
from app.shared.specifications import Specification
from app.structure.application.dao.pupils import PupilByIDs, PupilByParentID
from app.structure.application.dao.school_classes import ClassByIDs, ClassByNumberRange, ClassByTeacherID
from app.structure.domain.parent import ParentID
from app.structure.domain.pupil import Pupil
from app.structure.domain.school import School
from app.structure.domain.school_class import Number, SchoolClass
from app.structure.domain.teacher import TeacherID


@unique
class SchoolClassType(str, Enum):
    PRIMARY = "primary"
    HIGH = "high"


class PupilFilters(Filters[Pupil]):
    ids: set[str] | None = None
    parent_id: UUID | None = None

    def _build_map(self) -> dict[str, Callable[[Any], Specification[Pupil]]]:
        return {
            "ids": lambda x: PupilByIDs({PupilID(pupil_id) for pupil_id in x}),
            "parent_id": lambda x: PupilByParentID(ParentID(x)),
        }


class ClassesFilters(Filters[SchoolClass]):
    ids: set[UUID] | None = None
    teacher_id: UUID | None = None
    class_type: SchoolClassType | None = None

    def _build_map(self) -> dict[str, Callable[[Any], Specification[SchoolClass]]]:
        return {
            "ids": lambda x: ClassByIDs({ClassID(class_id) for class_id in x}),
            "teacher_id": lambda x: ClassByTeacherID(TeacherID(x)),
            "class_type": lambda x: ClassByNumberRange(start=Number(1), end=Number(4))
            if x is SchoolClassType.PRIMARY
            else ClassByNumberRange(start=Number(5), end=Number(11)),
        }


class FullNameOut(BaseModel):
    last: str
    first: str
    patronymic: str | None

    @classmethod
    def from_model(cls, name: FullName) -> "FullNameOut":
        return cls(
            last=name.last.value, first=name.first.value, patronymic=name.patronymic.value if name.patronymic else None
        )


class PupilOut(BaseModel):
    id: str
    name: FullNameOut
    class_id: UUID
    parent_ids: list[UUID]

    @classmethod
    def from_model(cls, pupil: Pupil) -> "PupilOut":
        return cls(
            id=pupil.id.value,
            name=FullNameOut.from_model(pupil.name),
            class_id=pupil.class_id.value,
            parent_ids=[parent_id.value for parent_id in pupil.parent_ids],
        )


class SchoolOut(BaseModel):
    name: str

    @classmethod
    def from_model(cls, school: School) -> "SchoolOut":
        return cls(name=school.name.value)


class SchoolClassOut(BaseModel):
    id: UUID
    teacher_id: UUID
    number: int
    literal: str

    @classmethod
    def from_model(cls, school_class: SchoolClass) -> "SchoolClassOut":
        return cls(
            id=school_class.id.value,
            teacher_id=school_class.teacher_id.value,
            number=school_class.number.value,
            literal=school_class.literal.value,
        )
