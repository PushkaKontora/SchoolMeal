from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.auth.db.sqlalchemy.repositories import AlchemyIssuedTokensRepository, AlchemyPasswordsRepository
from app.database.unit_of_work import UnitOfWork
from app.users.db.sqlalchemy.repositories import AlchemyUsersRepository


class AlchemyUnitOfWork(UnitOfWork):
    def __init__(
        self,
        session_maker: async_sessionmaker[AsyncSession],
        users_repository: type[AlchemyUsersRepository],
        passwords_repository: type[AlchemyPasswordsRepository],
        issued_tokens_repository: type[AlchemyIssuedTokensRepository],
    ):
        super().__init__()

        self._session = session_maker()

        self.users_repo = users_repository(self._session)
        self.passwords_repo = passwords_repository(self._session)
        self.issued_tokens_repo = issued_tokens_repository(self._session)

    async def _begin(self) -> None:
        await self._session.begin()

    async def _commit(self) -> None:
        await self._session.commit()

    async def _rollback(self) -> None:
        await self._session.rollback()

    async def _close(self) -> None:
        await self._session.close()
