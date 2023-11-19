from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.nutrition.application.repositories import IPupilsRepository, NotFoundPupil
from app.nutrition.domain.pupil import Pupil, PupilID
from app.nutrition.infrastructure.db.models import PupilDB


class PupilsRepository(IPupilsRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, pupil_id: PupilID) -> Pupil:
        try:
            query = select(PupilDB).where(PupilDB.id == pupil_id.value).limit(1)
            pupil_db: PupilDB = (await self._session.scalars(query)).one()
        except NoResultFound as error:
            raise NotFoundPupil from error

        return pupil_db.to_model()

    async def update(self, pupil: Pupil) -> None:
        pupil_db = PupilDB.from_model(pupil)

        query = update(PupilDB).values(pupil_db.dict()).where(PupilDB.id == pupil_db.id)
        await self._session.execute(query)
