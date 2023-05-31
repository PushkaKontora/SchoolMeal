from dependency_injector.wiring import Provide

from app.container import Container
from app.db.unit_of_work import UnitOfWork
from app.school_classes.db.school_class.filters import ByOptionTeacherId
from app.school_classes.db.school_class.joins import WithSchool
from app.school_classes.db.school_class.model import SchoolClass
from app.school_classes.domain.entities import ClassOut, SchoolClassesGetOptions


async def get_school_classes_by_options(
    options: SchoolClassesGetOptions, uow: UnitOfWork = Provide[Container.unit_of_work]
) -> list[ClassOut]:
    async with uow:
        school_classes = await uow.repository(SchoolClass).find(ByOptionTeacherId(options.teacher_id), WithSchool())

        return [ClassOut.from_orm(school_class) for school_class in school_classes]
