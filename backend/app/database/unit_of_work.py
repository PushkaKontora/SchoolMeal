from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.db.issued_token.model import IssuedToken
from app.auth.db.password.model import Password
from app.auth.domain.base_repositories import BaseIssuedTokensRepository, BasePasswordsRepository
from app.cancel_meal_periods.db.cancel_meal_period.model import CancelMealPeriod
from app.cancel_meal_periods.domain.base_repositories import BaseCancelMealPeriodsRepository
from app.children.db.parent_pupil.model import ParentPupil
from app.children.domain.base_repositories import BaseChildrenRepository
from app.foods.db.portion.model import Portion
from app.foods.domain.base_repositories import BasePortionsRepository
from app.meals.db.meal.model import Meal
from app.meals.domain.base_repositories import BaseMealsRepository
from app.pupils.db.pupil.model import Pupil
from app.pupils.domain.base_repositories import BasePupilsRepository
from app.users.db.user.model import User
from app.users.domain.base_repositories import BaseUsersRepository


class UnitOfWork:
    def __init__(
        self,
        session: AsyncSession,
        users_repository: type[BaseUsersRepository],
        passwords_repository: type[BasePasswordsRepository],
        issued_tokens_repository: type[BaseIssuedTokensRepository],
        pupils_repository: type[BasePupilsRepository],
        children_repository: type[BaseChildrenRepository],
        cancel_meal_periods_repository: type[BaseCancelMealPeriodsRepository],
        meals_repository: type[BaseMealsRepository],
        portions_repository: type[BasePortionsRepository],
    ):
        self._session = session

        self._users_repo = users_repository(self._session, User)
        self._passwords_repo = passwords_repository(self._session, Password)
        self._issued_tokens_repo = issued_tokens_repository(self._session, IssuedToken)
        self._pupils_repo = pupils_repository(self._session, Pupil)
        self._children_repo = children_repository(self._session, ParentPupil)
        self._cancel_meal_periods_repo = cancel_meal_periods_repository(self._session, CancelMealPeriod)
        self._meals_repo = meals_repository(self._session, Meal)
        self._portions_repo = portions_repository(self._session, Portion)

    @property
    def users_repo(self) -> BaseUsersRepository:
        return self._users_repo

    @property
    def passwords_repo(self) -> BasePasswordsRepository:
        return self._passwords_repo

    @property
    def issued_tokens_repo(self) -> BaseIssuedTokensRepository:
        return self._issued_tokens_repo

    @property
    def pupils_repo(self) -> BasePupilsRepository:
        return self._pupils_repo

    @property
    def children_repo(self) -> BaseChildrenRepository:
        return self._children_repo

    @property
    def cancel_meal_periods_repo(self) -> BaseCancelMealPeriodsRepository:
        return self._cancel_meal_periods_repo

    @property
    def portions_repo(self) -> BasePortionsRepository:
        return self._portions_repo

    @property
    def meals_repo(self) -> BaseMealsRepository:
        return self._meals_repo

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def __aenter__(self):
        await self._session.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()

        await self._session.close()
