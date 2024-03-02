from typing import AsyncContextManager, Callable

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.nutrition.application.dao import IPupilRepository
from app.nutrition.domain.pupil import Pupil, PupilID
from app.nutrition.domain.school_class import ClassID
from app.nutrition.infrastructure.db import PupilDB


class AlchemyPupilRepository(IPupilRepository):
    def __init__(self, session_factory: Callable[[], AsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def merge(self, pupil: Pupil) -> None:
        pupil_db = PupilDB.from_model(pupil).dict()

        query = (
            insert(PupilDB)
            .values(pupil_db)
            .on_conflict_do_update(
                index_elements=[PupilDB.id],
                set_=pupil_db,
            )
        )

        async with self._session_factory() as session:
            await session.execute(query)
            await session.commit()

    async def get_by_id(self, id_: PupilID) -> Pupil | None:
        async with self._session_factory() as session:
            pupil_db = await session.get(PupilDB, ident=id_.value)

            return pupil_db.to_model() if pupil_db else None

    async def all_by_class_id(self, class_id: ClassID) -> list[Pupil]:
        query = select(PupilDB).where(PupilDB.class_id == class_id.value)

        async with self._session_factory() as session:
            return [pupil_db.to_model() for pupil_db in (await session.scalars(query)).all()]
