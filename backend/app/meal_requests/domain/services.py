from dependency_injector.wiring import Provide

from app.container import Container
from app.db.unit_of_work import UnitOfWork
from app.meal_requests.db.declared_pupil.model import DeclaredPupil
from app.meal_requests.db.meal_request.filters import ByMealId
from app.meal_requests.db.meal_request.model import MealRequest
from app.meal_requests.domain.entities import MealRequestIn, MealRequestOut
from app.meal_requests.domain.errors import (
    InvalidPupilsSequenceError,
    MealDoesNotExistError,
    MealRequestAlreadyExistsError,
    NotFoundCreatorError,
)
from app.meals.db.meal.filters import ById
from app.meals.db.meal.joins import WithSchoolClass
from app.meals.db.meal.model import Meal
from app.pupils.db.pupil.filters import ByClassId
from app.pupils.db.pupil.model import Pupil
from app.users.db.user.filters import ByUserId
from app.users.db.user.model import User


async def create_request_by_user(
    user_id: int, data: MealRequestIn, uow: UnitOfWork = Provide[Container.unit_of_work]
) -> MealRequestOut:
    async with uow:
        if not await uow.repository(User).exists(ByUserId(user_id)):
            raise NotFoundCreatorError

        if await uow.repository(MealRequest).exists(ByMealId(data.meal_id)):
            raise MealRequestAlreadyExistsError

        meal = await uow.repository(Meal).find_first(ById(data.meal_id), WithSchoolClass())
        if not meal:
            raise MealDoesNotExistError

        pupils = await uow.repository(Pupil).find(ByClassId(meal.school_class.id))
        if set(p.id for p in data.pupils) != set(p.id for p in pupils):
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
