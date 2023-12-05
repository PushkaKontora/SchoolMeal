from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.shared.db.settings import DatabaseSettings
from app.shared.unit_of_work import IRootSession, ISession


def get_session_cls(settings: DatabaseSettings) -> type[AsyncSession]:
    return sessionmaker(  # type: ignore
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
        bind=create_async_engine(url=settings.url, pool_size=settings.pool_size),
    )


class AlchemySession(IRootSession):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def begin(self) -> None:
        await self._session.begin()

    async def close(self) -> None:
        await self._session.close()

    async def begin_nested(self) -> "ISession":
        return AlchemySession(session=await self._session.begin_nested())

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
