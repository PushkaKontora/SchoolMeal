from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.db.models import IssuedToken, Password
from app.auth.domain.base_repositories import BaseIssuedTokensRepository, BasePasswordsRepository
from app.children.db.models import Child
from app.children.domain.base_repositories import BaseChildrenRepository
from app.pupils.db.models import Pupil
from app.pupils.domain.base_repositories import BasePupilsRepository
from app.users.db.models import User
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
    ):
        self._session = session

        self._users_repo = users_repository(self._session, User)
        self._passwords_repo = passwords_repository(self._session, Password)
        self._issued_tokens_repo = issued_tokens_repository(self._session, IssuedToken)
        self._pupils_repo = pupils_repository(self._session, Pupil)
        self._children_repo = children_repository(self._session, Child)

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
