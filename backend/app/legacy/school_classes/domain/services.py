from dependency_injector.wiring import Provide

from app.legacy.container import AppContainer
from app.legacy.db.unit_of_work import UnitOfWork
from app.legacy.school_classes.db.school_class.filters import ByOptionTeacherId
from app.legacy.school_classes.db.school_class.joins import WithSchool
from app.legacy.school_classes.db.school_class.model import SchoolClass
from app.legacy.school_classes.domain.entities import ClassWithSchoolOut, SchoolClassesGetOptions


async def get_school_classes_by_options(
    options: SchoolClassesGetOptions, uow: UnitOfWork = Provide[AppContainer.unit_of_work]
) -> list[ClassWithSchoolOut]:
    async with uow:
        school_classes = await uow.repository(SchoolClass).find(ByOptionTeacherId(options.teacher_id), WithSchool())

        return [ClassWithSchoolOut.from_orm(school_class) for school_class in school_classes]
