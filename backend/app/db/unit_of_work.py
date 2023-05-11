from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repository import Repository, TModel


class TransactionHasNotStartedException(Exception):
    pass


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._repositories = {}
        self._is_began = False

    def repository(self, model: type[TModel]) -> Repository[TModel]:
        if not self._is_began:
            raise TransactionHasNotStartedException

        self._repositories[model] = self._repositories[model] or Repository(self._session, model)

        return self._repositories[model]

    async def commit(self) -> None:
        if not self._is_began:
            raise TransactionHasNotStartedException

        await self._session.commit()

    async def rollback(self) -> None:
        if not self._is_began:
            raise TransactionHasNotStartedException

        await self._session.rollback()

    async def begin(self) -> None:
        self._is_began = True
        self._repositories.clear()

        await self._session.begin()

    async def close(self) -> None:
        if not self._is_began:
            raise TransactionHasNotStartedException

        self._is_began = False
        self._repositories.clear()

        await self._session.close()

    async def __aenter__(self):
        await self.begin()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()

        await self.close()
