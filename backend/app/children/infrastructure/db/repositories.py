from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.children.application.repositories import IChildrenRepository, IParentsRepository, NotFoundChild, NotFoundParent
from app.children.domain.child import Child, ChildID
from app.children.domain.parent import Parent
from app.children.infrastructure.db.models import ChildDB, ParentDB


class ParentsRepository(IParentsRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, parent_id: UUID) -> Parent:
        try:
            query = select(ParentDB).where(ParentDB.id == parent_id).limit(1)
            parent_db: ParentDB = (await self._session.scalars(query)).one()
        except NoResultFound as error:
            raise NotFoundParent from error

        return parent_db.to_model()

    async def update(self, parent: Parent) -> None:
        parent_db = ParentDB.from_model(parent)

        query = update(ParentDB).values(**parent_db.dict()).where(ParentDB.id == parent_db.id)
        await self._session.execute(query)


class ChildrenRepository(IChildrenRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, child_id: ChildID) -> Child:
        try:
            query = select(ChildDB).where(ChildDB.id == child_id.value).limit(1)
            child_db: ChildDB = (await self._session.scalars(query)).one()
        except NoResultFound as error:
            raise NotFoundChild from error

        return child_db.to_model()

    async def get_all_by_ids(self, ids: set[ChildID]) -> list[Child]:
        query = select(ChildDB).where(ChildDB.id.in_({child_id.value for child_id in ids}))
        children_db: list[ChildDB] = (await self._session.scalars(query)).all()

        return [child_db.to_model() for child_db in children_db]
