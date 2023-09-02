from datetime import time
from typing import Iterable

from dependency_injector.wiring import Provide

from app.legacy.container import AppContainer
from app.legacy.db.unit_of_work import UnitOfWork
from app.legacy.meal_requests.db.declared_pupil.filters import DeclaredPupilFilters
from app.legacy.meal_requests.db.declared_pupil.model import DeclaredPupil
from app.legacy.meal_requests.db.meal_request import filters as meal_request_filters
from app.legacy.meal_requests.db.meal_request.model import MealRequest
from app.legacy.meal_requests.domain.entities import (
    DeclaredPupilSchema,
    ExtendedMealRequestOut,
    MealRequestIn,
    MealRequestOut,
    MealRequestPutIn,
    MealRequestsGetOptions,
)
from app.legacy.meal_requests.domain.errors import (
    InvalidPupilsSequenceError,
    MealDoesNotExistError,
    MealRequestAlreadyExistsError,
    NotFoundCreatorError,
    NotFoundMealRequestError,
    UpdatingFrozenRequestError,
)
from app.legacy.meals.db.meal import filters as meal_filters, joins as meal_joins
from app.legacy.meals.db.meal.model import Meal
from app.legacy.pupils.db.pupil import filters as pupil_filters
from app.legacy.pupils.db.pupil.model import Pupil
from app.legacy.school_classes.db.school_class.model import SchoolClass
from app.legacy.school_classes.domain.entities import ClassOut
from app.legacy.users.db.user import filters as user_filters
from app.legacy.users.db.user.model import User
from app.legacy.utils import timezone


async def get_requests_by_options(
    options: MealRequestsGetOptions, uow: UnitOfWork = Provide[AppContainer.unit_of_work]
) -> list[ExtendedMealRequestOut]:
    async with uow:
        meals = await uow.repository(Meal).find(
            meal_filters.BySomeSchoolId(options.school_id),
            meal_filters.BySomeDate(options.date),
            meal_joins.WithSchoolClass(),
            meal_joins.WithRequest(),
            meal_joins.WithDeclaredPupils(),
        )

        return [
            ExtendedMealRequestOut(
                id=request.id,
                creator_id=request.creator_id,
                meal_id=request.meal_id,
                date=request.meal.date,
                created_at=request.created_at,
                pupils=[
                    DeclaredPupilSchema(
                        id=p.pupil_id,
                        breakfast=p.breakfast,
                        lunch=p.lunch,
                        dinner=p.dinner,
                        preferential=p.preferential,
                    )
                    for p in request.declared_pupils
                ],
                school_class=ClassOut.from_orm(request.meal.school_class),
            )
            for request in (meal.request for meal in meals)
        ]


async def create_request_by_user(
    user_id: int, data: MealRequestIn, uow: UnitOfWork = Provide[AppContainer.unit_of_work]
) -> MealRequestOut:
    async with uow:
        if not await uow.repository(User).exists(user_filters.ByUserId(user_id)):
            raise NotFoundCreatorError

        if await uow.repository(MealRequest).exists(meal_request_filters.ByMealId(data.meal_id)):
            raise MealRequestAlreadyExistsError

        meal = await uow.repository(Meal).find_first(meal_filters.ById(data.meal_id), meal_joins.WithSchoolClass())
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
    request_id: int,
    data: MealRequestPutIn,
    uow: UnitOfWork = Provide[AppContainer.unit_of_work],
) -> MealRequestOut:
    async with uow:
        request = await uow.repository(MealRequest).find_first(meal_request_filters.ById(request_id))
        if not request:
            raise NotFoundMealRequestError

        meal = await uow.repository(Meal).get_one(meal_filters.ById(request.meal_id), meal_joins.WithSchoolClass())
        if not await _match_pupils_with_pupils_in_school_class(uow, data.pupils, meal.school_class):
            raise InvalidPupilsSequenceError

        if timezone.now() > timezone.combine(meal.date, time(hour=10)):
            raise UpdatingFrozenRequestError

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
    uow: UnitOfWork, actual: Iterable[DeclaredPupilSchema], school_class: SchoolClass
) -> bool:
    pupils = await uow.repository(Pupil).find(pupil_filters.ByClassId(school_class.id))

    return set(p.id for p in actual) == set(p.id for p in pupils)
