from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.application.repositories import IUserRepository
from app.user.domain.errors import NotFoundUserError
from app.user.domain.model import Login, User, UserID
from app.user.infrastructure.db.models import UserDB


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, user: User) -> None:
        user_db = UserDB.from_domain(user)

        self._session.add(user_db)
        await self._session.flush([user_db])

    async def get_by_login(self, login: Login) -> User:
        try:
            query = select(UserDB).where(UserDB.login == login.value).limit(1)
            user_db: UserDB = (await self._session.scalars(query)).one()
        except NoResultFound as error:
            raise NotFoundUserError from error

        return user_db.to_domain()

    async def get_by_id(self, user_id: UserID) -> User:
        try:
            query = select(UserDB).where(UserDB.id == user_id.value).limit(1)
            user_db: UserDB = (await self._session.scalars(query)).one()
        except NoResultFound as error:
            raise NotFoundUserError from error

        return user_db.to_domain()

    async def update_refresh_tokens_at(self, user: User) -> None:
        await self._session.execute(
            update(UserDB)
            .where(UserDB.id == user.id.value)
            .values(authenticated_ips={str(ip): str(token) for ip, token in user.authenticated_ips.items()})
        )
