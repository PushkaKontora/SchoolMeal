from dependency_injector.wiring import Provide, inject

from app.legacy.cancel_meal_periods.domain.entities import PeriodOut
from app.legacy.children.db.child.filters import ByParentId, ByPupilId
from app.legacy.children.db.child.model import Child
from app.legacy.children.db.child.selectors import OnlyPupilId
from app.legacy.children.domain.entities import ChildIn, PlanIn, PlanOut
from app.legacy.children.domain.errors import (
    NotFoundChildError,
    NotFoundParentError,
    NotUniqueChildError,
    UserIsNotParentOfThePupilError,
)
from app.legacy.container import AppContainer
from app.legacy.db.specifications import ForUpdate
from app.legacy.db.unit_of_work import UnitOfWork
from app.legacy.pupils.db.pupil.filters import ById as PupilById, ByIds
from app.legacy.pupils.db.pupil.joins import WithCancelMealPeriods, WithClass, WithSchool, WithTeachers
from app.legacy.pupils.db.pupil.model import Pupil
from app.legacy.pupils.domain.entities import PupilWithClassAndPeriodsOut
from app.legacy.school_classes.db.school_class.model import SchoolClass
from app.legacy.school_classes.domain.entities import ClassWithTeachersOut
from app.legacy.schools.domain.entities import SchoolOut
from app.legacy.users.db.user.filters import ByUserId as UserById
from app.legacy.users.db.user.model import User
from app.legacy.users.domain.entities import ContactOut


@inject
async def get_child_by_id(
    parent_id: int, child_id: str, uow: UnitOfWork = Provide[AppContainer.unit_of_work]
) -> PupilWithClassAndPeriodsOut:
    async with uow:
        if not await uow.repository(Child).exists(ByParentId(parent_id) & ByPupilId(child_id)):
            raise UserIsNotParentOfThePupilError

        pupil = await uow.repository(Pupil).get_one(
            PupilById(child_id), WithClass(), WithSchool(), WithTeachers(), WithCancelMealPeriods()
        )

        return _get_child_out(pupil)


@inject
async def add_pupil_to_children(
    parent_id: int, child: ChildIn, uow: UnitOfWork = Provide[AppContainer.unit_of_work]
) -> None:
    async with uow:
        if not await uow.repository(User).exists(UserById(parent_id)):
            raise NotFoundParentError

        if not await uow.repository(Pupil).exists(PupilById(child.child_id)):
            raise NotFoundChildError

        if await uow.repository(Child).exists(ByParentId(parent_id) & ByPupilId(child.child_id)):
            raise NotUniqueChildError

        uow.repository(Child).save(Child(parent_id=parent_id, pupil_id=child.child_id))
        await uow.commit()


@inject
async def get_children_by_parent_id(
    parent_id: int, uow: UnitOfWork = Provide[AppContainer.unit_of_work]
) -> list[PupilWithClassAndPeriodsOut]:
    async with uow:
        children = await uow.repository(Child).find(ByParentId(parent_id), OnlyPupilId())
        child_ids = set(child.pupil_id for child in children)

        children = await uow.repository(Pupil).find(
            ByIds(child_ids), WithClass(), WithSchool(), WithTeachers(), WithCancelMealPeriods()
        )

        return [_get_child_out(child) for child in children]


@inject
async def change_meal_plan_by_parent_id(
    parent_id: int,
    child_id: str,
    plan: PlanIn,
    uow: UnitOfWork = Provide[AppContainer.unit_of_work],
) -> PlanOut:
    async with uow:
        if not await uow.repository(Child).exists(ByParentId(parent_id) & ByPupilId(child_id)):
            raise UserIsNotParentOfThePupilError

        child = await uow.repository(Pupil).find_first(PupilById(child_id), ForUpdate())
        child.breakfast = plan.breakfast if plan.breakfast is not None else child.breakfast
        child.lunch = plan.lunch if plan.lunch is not None else child.lunch
        child.dinner = plan.dinner if plan.dinner is not None else child.dinner

        uow.repository(Pupil).save(child)
        await uow.commit()
        await uow.repository(Pupil).refresh(child)

        return PlanOut(
            breakfast=child.breakfast,
            lunch=child.lunch,
            dinner=child.dinner,
        )


def _get_child_out(child: Pupil) -> PupilWithClassAndPeriodsOut:
    school_class: SchoolClass | None = child.school_class
    school_class_out = (
        ClassWithTeachersOut(
            id=school_class.id,
            number=school_class.number,
            letter=school_class.letter,
            has_breakfast=school_class.has_breakfast,
            has_lunch=school_class.has_lunch,
            has_dinner=school_class.has_dinner,
            teachers=[ContactOut.from_orm(teacher) for teacher in school_class.teachers],
            school=SchoolOut.from_orm(school_class.school),
        )
        if school_class
        else None
    )

    return PupilWithClassAndPeriodsOut(
        id=child.id,
        last_name=child.last_name,
        first_name=child.first_name,
        certificate_before_date=child.certificate_before_date,
        balance=child.balance,
        breakfast=child.breakfast,
        lunch=child.lunch,
        dinner=child.dinner,
        school_class=school_class_out,
        cancel_meal_periods=[PeriodOut.from_orm(period) for period in child.cancel_meal_periods],
    )
