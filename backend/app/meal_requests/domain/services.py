from typing import Iterable

from dependency_injector.wiring import Provide

from app.container import Container
from app.db.unit_of_work import UnitOfWork
from app.meal_requests.db.declared_pupil.filters import DeclaredPupilFilters
from app.meal_requests.db.declared_pupil.model import DeclaredPupil
from app.meal_requests.db.meal_request.filters import MealRequestFilters
from app.meal_requests.db.meal_request.model import MealRequest
from app.meal_requests.domain.entities import DeclaredPupilIn, MealRequestIn, MealRequestOut, MealRequestPutIn
from app.meal_requests.domain.errors import (
    InvalidPupilsSequenceError,
    MealDoesNotExistError,
    MealRequestAlreadyExistsError,
    NotFoundCreatorError,
    NotFoundMealRequestError,
)
from app.meals.db.meal.filters import ById
from app.meals.db.meal.joins import WithSchoolClass
from app.meals.db.meal.model import Meal
from app.pupils.db.pupil.filters import ByClassId
from app.pupils.db.pupil.model import Pupil
from app.school_classes.db.school_class.model import SchoolClass
from app.users.db.user.filters import ByUserId
from app.users.db.user.model import User


async def create_request_by_user(
    user_id: int, data: MealRequestIn, uow: UnitOfWork = Provide[Container.unit_of_work]
) -> MealRequestOut:
    async with uow:
        if not await uow.repository(User).exists(ByUserId(user_id)):
            raise NotFoundCreatorError

        if await uow.repository(MealRequest).exists(MealRequestFilters.ByMealId(data.meal_id)):
            raise MealRequestAlreadyExistsError

        meal = await uow.repository(Meal).find_first(ById(data.meal_id), WithSchoolClass())
        if not meal:
            raise MealDoesNotExistError

        if not await _match_pupils_with_pupils_in_school_class(uow, data.pupils, meal.school_class):
            raise InvalidPupilsSequenceError

        request = MealRequest(
            creator_id=user_id,
            meal_id=meal.id,
            declared_pupils=[
                DeclaredPupil(
                    pupil_id=p.id, breakfast=p.breakfast, lunch=p.lunch, dinner=p.dinner, preferential=p.preferential
                )
                for p in data.pupils
            ],
        )
        uow.repository(MealRequest).save(request)
        await uow.commit()
        await uow.repository(MealRequest).refresh(request)

        return MealRequestOut.from_orm(request)


async def update_request(
    request_id: int, data: MealRequestPutIn, uow: UnitOfWork = Provide[Container.unit_of_work]
) -> MealRequestOut:
    async with uow:
        request = await uow.repository(MealRequest).find_first(MealRequestFilters.ById(request_id))
        if not request:
            raise NotFoundMealRequestError

        meal = await uow.repository(Meal).get_one(ById(request.meal_id), WithSchoolClass())
        if not await _match_pupils_with_pupils_in_school_class(uow, data.pupils, meal.school_class):
            raise InvalidPupilsSequenceError

        await uow.repository(DeclaredPupil).delete_many(DeclaredPupilFilters.ByRequestId(request.id))
        updated_pupils = [
            DeclaredPupil(
                request_id=request.id,
                pupil_id=p.id,
                breakfast=p.breakfast,
                lunch=p.lunch,
                dinner=p.dinner,
                preferential=p.preferential,
            )
            for p in data.pupils
        ]
        for new_pupil in updated_pupils:
            uow.repository(DeclaredPupil).save(new_pupil)

        await uow.commit()
        await uow.repository(MealRequest).refresh(request)

        return MealRequestOut.from_orm(request)


async def _match_pupils_with_pupils_in_school_class(
    uow: UnitOfWork, actual: Iterable[DeclaredPupilIn], school_class: SchoolClass
) -> bool:
    pupils = await uow.repository(Pupil).find(ByClassId(school_class.id))

    return set(p.id for p in actual) == set(p.id for p in pupils)
