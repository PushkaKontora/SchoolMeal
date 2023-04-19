from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.auth.db.models import IssuedToken, Password
from app.auth.domain.base_repositories import BaseIssuedTokensRepository, BasePasswordsRepository
from app.users.db.models import User
from app.users.domain.base_repositories import BaseUsersRepository


class UnitOfWork:
    users_repo: BaseUsersRepository
    passwords_repo: BasePasswordsRepository
    issued_tokens_repo: BaseIssuedTokensRepository

    def __init__(
        self,
        session_maker: async_sessionmaker[AsyncSession],
        users_repository: type[BaseUsersRepository],
        passwords_repository: type[BasePasswordsRepository],
        issued_tokens_repository: type[BaseIssuedTokensRepository],
    ):
        self._session = session_maker()

        self._users_repo = users_repository(self._session, User)
        self._passwords_repo = passwords_repository(self._session, Password)
        self._issued_tokens_repo = issued_tokens_repository(self._session, IssuedToken)

    @property
    def session(self) -> AsyncSession:
        return self._session

    @property
    def users_repo(self) -> BaseUsersRepository:
        return self._users_repo

    @property
    def passwords_repo(self) -> BasePasswordsRepository:
        return self._passwords_repo

    @property
    def issued_tokens_repo(self) -> BaseIssuedTokensRepository:
        return self._issued_tokens_repo

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
