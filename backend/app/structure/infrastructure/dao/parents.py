from typing import AsyncContextManager, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.domain.user import UserID
from app.structure.application.dao.parents import IParentRepository
from app.structure.domain.parent import Parent
from app.structure.infrastructure.db import ParentDB


class AlchemyParentRepository(IParentRepository):
    def __init__(self, session_factory: Callable[[], AsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def get(self, ident: UserID) -> Parent | None:
        async with self._session_factory() as session:
            parent_db = await session.get(ParentDB, ident=ident.value)

            return parent_db.to_model() if parent_db else None
