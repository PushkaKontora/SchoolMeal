from sqlalchemy import select

from app.database.specifications import FilterSpecification
from app.database.sqlalchemy.base import AlchemyRepository
from app.users.db.repositories import IUsersRepository
from app.users.db.sqlalchemy.models import User as UserModel
from app.users.domain.entities import User


class AlchemyUsersRepository(IUsersRepository, AlchemyRepository):
    async def get_one(self, specification: FilterSpecification) -> User | None:
        query = specification.to_query(select(UserModel).limit(1))
        user = await self.session.scalar(query)

        return User.from_orm(user) if user else None
