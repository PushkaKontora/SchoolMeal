from typing import AsyncContextManager, Callable

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.nutrition.application.dao.pupils import IPupilRepository
from app.nutrition.domain.pupil import Pupil, PupilID
from app.nutrition.infrastructure.db import PupilDB, PupilParentAssociation
from app.shared.specifications import Specification


class AlchemyPupilRepository(IPupilRepository):
    def __init__(self, session_factory: Callable[[], AsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def merge(self, pupil: Pupil) -> None:
        pupil_db = PupilDB.from_model(pupil)
        pupil_dict = pupil_db.dict()

        query = (
            insert(PupilDB)
            .values(pupil_dict)
            .on_conflict_do_update(
                index_elements=[PupilDB.id],
                set_=pupil_dict,
            )
        )
        delete_parents = delete(PupilParentAssociation).where(PupilParentAssociation.pupil_id == pupil_db.id)

        async with self._session_factory() as session:
            await session.execute(query)

            await session.execute(delete_parents)
            session.add_all(
                (
                    PupilParentAssociation(pupil_id=pupil_db.id, parent_id=parent_id.value)
                    for parent_id in pupil.parent_ids
                )
            )

            await session.commit()

    async def get(self, ident: PupilID) -> Pupil | None:
        async with self._session_factory() as session:
            pupil_db = await session.get(PupilDB, ident=ident.value)

            return pupil_db.to_model() if pupil_db else None

    async def all(self, spec: Specification[Pupil] | None = None) -> list[Pupil]:
        query = select(PupilDB).order_by(
            PupilDB.last_name.asc(),
            PupilDB.first_name.asc(),
            PupilDB.patronymic.asc().nulls_last(),
        )

        async with self._session_factory() as session:
            pupils = (pupil_db.to_model() for pupil_db in (await session.scalars(query)).all())

            return list(filter(lambda x: spec.is_satisfied_by(x), pupils) if spec else pupils)
