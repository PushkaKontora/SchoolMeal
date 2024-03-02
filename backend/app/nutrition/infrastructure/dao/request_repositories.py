from typing import AsyncContextManager, Callable

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.nutrition.application.dao import IRequestRepository
from app.nutrition.domain.request import Request
from app.nutrition.infrastructure.db import RequestDB


class AlchemyRequestRepository(IRequestRepository):
    def __init__(self, session_factory: Callable[[], AsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

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
