from datetime import date
from typing import Any, Callable
from uuid import UUID

from app.nutrition.api.v1.schemas.enums import SchoolClassTypeDTO
from app.nutrition.application.dao.pupils import PupilByClassID, PupilByParentID
from app.nutrition.application.dao.school_classes import ClassByTeacherID
from app.nutrition.domain.parent import ParentID
from app.nutrition.domain.pupil import Pupil
from app.nutrition.domain.school_class import ClassID, SchoolClass
from app.nutrition.domain.teacher import TeacherID
from app.shared.api.schemas import Filters, FrontendParams
from app.shared.specifications import Specification


class GetPortionsParams(FrontendParams):
    class_type: SchoolClassTypeDTO
    on_date: date


class RequestIDParams(FrontendParams):
    class_id: UUID
    on_date: date


class GetSchoolClassesParams(Filters[SchoolClass]):
    teacher_id: UUID | None = None

    def _build_map(self) -> dict[str, Callable[[Any], Specification[SchoolClass]]]:
        return {
            "teacher_id": lambda x: ClassByTeacherID(TeacherID(x)),
        }


class GetPupilsParams(Filters[Pupil]):
    class_id: UUID | None = None
    parent_id: UUID | None = None

    def _build_map(self) -> dict[str, Callable[[Any], Specification[Pupil]]]:
        return {
            "class_id": lambda x: PupilByClassID(ClassID(x)),
            "parent_id": lambda x: PupilByParentID(ParentID(x)),
        }
