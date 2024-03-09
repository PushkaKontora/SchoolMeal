from datetime import date
from typing import AsyncContextManager, Callable

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.nutrition.application.dao.requests import IRequestRepository
from app.nutrition.domain.request import Request
from app.nutrition.infrastructure.db import RequestDB
from app.shared.domain.school_class import ClassID


class AlchemyRequestRepository(IRequestRepository):
    def __init__(self, session_factory: Callable[[], AsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def add(self, request: Request) -> None:
        request_db = RequestDB.from_model(request)

        async with self._session_factory() as session:
            session.add(request_db)
            await session.commit()

    async def merge(self, request: Request) -> None:
        request_db = RequestDB.from_model(request).dict()

        query = (
            insert(RequestDB)
            .values(request_db)
            .on_conflict_do_update(
                index_elements=[RequestDB.class_id, RequestDB.on_date],
                set_=request_db,
            )
        )

        async with self._session_factory() as session:
            await session.execute(query)
            await session.commit()

    async def exists(self, class_id: ClassID, on_date: date) -> bool:
        query = (
            select(1)
            .select_from(RequestDB)
            .where(RequestDB.class_id == class_id.value, RequestDB.on_date == on_date)
            .limit(1)
        )

        async with self._session_factory() as session:
            result = await session.scalar(query)

            return bool(result)

    async def get(self, class_id: ClassID, on_date: date) -> Request | None:
        async with self._session_factory() as session:
            request_db = await session.get(RequestDB, ident=(class_id.value, on_date))

            return request_db.to_model() if request_db else None
