from typing import AsyncContextManager, Callable

from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.domain.pupil import PupilID
from app.structure.application.dao.pupils import IPupilRepository
from app.structure.domain.pupil import Pupil
from app.structure.infrastructure.db import PupilDB, PupilParentAssociation


class AlchemyPupilRepository(IPupilRepository):
    def __init__(self, session_factory: Callable[[], AsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def get(self, ident: PupilID) -> Pupil | None:
        async with self._session_factory() as session:
            pupil_db = await session.get(PupilDB, ident=ident.value)

            return pupil_db.to_model() if pupil_db else None

    async def merge(self, pupil: Pupil) -> None:
        pupil_db = PupilDB.from_model(pupil)
        associations = PupilParentAssociation.from_model(pupil)

        pupil_dict = pupil_db.dict()
        upsert_query = (
            insert(PupilDB).values(pupil_dict).on_conflict_do_update(index_elements=[PupilDB.id], set_=pupil_dict)
        )
        delete_associations = delete(PupilParentAssociation).where(PupilParentAssociation.pupil_id == pupil_db.id)

        async with self._session_factory() as session:
            await session.execute(upsert_query)

            await session.execute(delete_associations)
            session.add_all(associations)

            await session.commit()
