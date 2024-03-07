from typing import AsyncContextManager, Callable

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.nutrition.application.dao.parents import IParentRepository
from app.nutrition.domain.parent import Parent, ParentID
from app.nutrition.infrastructure.db import ParentDB


class AlchemyParentRepository(IParentRepository):
    def __init__(self, session_factory: Callable[[], AsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def merge(self, parent: Parent) -> None:
        parent_db = ParentDB.from_model(parent).dict()

        query = (
            insert(ParentDB)
            .values(parent_db)
            .on_conflict_do_update(
                index_elements=[ParentDB.id],
                set_=parent_db,
            )
        )

        async with self._session_factory() as session:
            await session.execute(query)
            await session.commit()

    async def get(self, ident: ParentID) -> Parent | None:
        async with self._session_factory() as session:
            parent_db = await session.get(ParentDB, ident=ident.value)

            return parent_db.to_model() if parent_db else None
