from typing import AsyncContextManager, Callable

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.nutrition.application.dao import IPupilDAO
from app.nutrition.domain.pupil import Pupil, PupilID
from app.nutrition.infrastructure.db.models import PupilDB


class AlchemyPupilDAO(IPupilDAO):
    def __init__(self, session_factory: Callable[[], AsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def update(self, pupil: Pupil) -> None:
        async with self._session_factory() as session:
            pupil_db = PupilDB.from_model(pupil)

            await session.execute(update(PupilDB).values(pupil_db.dict()).where(PupilDB.id == pupil_db.id))
            await session.commit()

    async def get_by_id(self, id_: PupilID) -> Pupil | None:
        async with self._session_factory() as session:
            pupil_db = await session.get(PupilDB, ident=id_.value)

            return pupil_db.to_model() if pupil_db else None
