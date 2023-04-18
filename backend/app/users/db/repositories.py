from sqlalchemy import select

from app.database.specifications import FilterSpecification
from app.users.db.models import User as UserModel
from app.users.domain.base_repositories import BaseUsersRepository
from app.users.domain.entities import User


class UsersRepository(BaseUsersRepository):
    async def find_one(self, specification: FilterSpecification) -> User | None:
        query = specification(select(UserModel).limit(1))
        user = await self.session.scalar(query)

        return User.from_orm(user) if user else None

    async def get_one(self, specification: FilterSpecification) -> User:
        query = specification(select(UserModel).limit(1))
        user = (await self.session.execute(query)).scalar_one()

        return User.from_orm(user)
