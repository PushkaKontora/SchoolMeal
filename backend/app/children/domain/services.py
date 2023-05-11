from dependency_injector.wiring import Provide, inject

from app.children.db.parent_pupil.filters import ByParentId, ByPupilId
from app.children.db.parent_pupil.model import ParentPupil
from app.children.domain.entities import ChildIn, ChildOut, ClassOut, PeriodOut, PlanIn, PlanOut, SchoolOut, TeacherOut
from app.children.domain.exceptions import (
    NotFoundChildException,
    NotFoundParentException,
    NotUniqueChildException,
    UserIsNotParentOfThePupilException,
)
from app.database.container import Database
from app.database.specifications import ForUpdate
from app.database.unit_of_work import UnitOfWork
from app.pupils.db.pupil.filters import ById as PupilById, ByIds
from app.pupils.db.pupil.joins import WithCancelMealPeriods, WithClass, WithSchool, WithTeachers
from app.pupils.db.pupil.model import Pupil
from app.school_classes.db.school_class.model import SchoolClass
from app.users.db.user.filters import ByUserId as UserById


@inject
async def add_pupil_to_parent_children(
    parent_id: int, child: ChildIn, uow: UnitOfWork = Provide[Database.unit_of_work]
) -> None:
    async with uow:
        if not await uow.users_repo.exists(UserById(parent_id)):
            raise NotFoundParentException

        if not await uow.pupils_repo.exists(PupilById(child.child_id)):
            raise NotFoundChildException

        if await uow.children_repo.exists(ByParentId(parent_id) & ByPupilId(child.child_id)):
            raise NotUniqueChildException

        uow.children_repo.save(ParentPupil(parent_id=parent_id, pupil_id=child.child_id))
        await uow.commit()


@inject
async def get_parent_children(parent_id: int, uow: UnitOfWork = Provide[Database.unit_of_work]) -> list[ChildOut]:
    async with uow:
        ids = await uow.children_repo.get_children_ids(ByParentId(parent_id))

        children = await uow.pupils_repo.find(
            ByIds(ids), WithClass(), WithSchool(), WithTeachers(), WithCancelMealPeriods()
        )

        return [_get_child_out(child) for child in children]


@inject
async def change_meal_plan_by_parent(
    parent_id: int,
    child_id: str,
    plan: PlanIn,
    uow: UnitOfWork = Provide[Database.unit_of_work],
) -> PlanOut:
    async with uow:
        if not await uow.children_repo.exists(ByParentId(parent_id) & ByPupilId(child_id)):
            raise UserIsNotParentOfThePupilException

        child = await uow.pupils_repo.find_one(PupilById(child_id), ForUpdate())
        child.breakfast = plan.breakfast if plan.breakfast is not None else child.breakfast
        child.lunch = plan.lunch if plan.lunch is not None else child.lunch
        child.dinner = plan.dinner if plan.dinner is not None else child.dinner

        uow.pupils_repo.save(child)
        await uow.commit()
        await uow.pupils_repo.refresh(child)

        return PlanOut(
            breakfast=child.breakfast,
            lunch=child.lunch,
            dinner=child.dinner,
        )


def _get_child_out(child: Pupil) -> ChildOut:
    school_class: SchoolClass | None = child.school_class
    school_class_out = (
        ClassOut(
            id=school_class.id,
            number=school_class.number,
            letter=school_class.letter,
            has_breakfast=school_class.has_breakfast,
            has_lunch=school_class.has_lunch,
            has_dinner=school_class.has_dinner,
            teachers=[TeacherOut.from_orm(teacher) for teacher in school_class.teachers],
            school=SchoolOut.from_orm(school_class.school),
        )
        if school_class
        else None
    )

    return ChildOut(
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
