from datetime import date
from typing import AsyncContextManager, Callable

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.nutrition.application.dao import IPupilDAO, IRequestDAO, ISchoolClassDAO
from app.nutrition.domain.pupil import Pupil, PupilID
from app.nutrition.domain.request import Request
from app.nutrition.domain.school_class import ClassID, SchoolClass
from app.nutrition.infrastructure.db.models import PupilDB, RequestDB, SchoolClassDB


SessionFactory = Callable[[], AsyncContextManager[AsyncSession]]


class AlchemyPupilDAO(IPupilDAO):
    def __init__(self, session_factory: SessionFactory) -> None:
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

    async def get_all_by_class_id(self, class_id: ClassID) -> list[Pupil]:
        async with self._session_factory() as session:
            query = select(PupilDB).where(PupilDB.class_id == class_id.value)
            pupils_db = (await session.scalars(query)).all()

            return [pupil_db.to_model() for pupil_db in pupils_db]


class AlchemySchoolClassDAO(ISchoolClassDAO):
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    async def get_by_id(self, id_: ClassID) -> SchoolClass | None:
        async with self._session_factory() as session:
            school_class = await session.get(SchoolClassDB, ident=id_.value)

            return school_class.to_model() if school_class else None


class AlchemyRequestDAO(IRequestDAO):
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    async def upsert(self, request: Request) -> None:
        async with self._session_factory() as session:
            request_db = RequestDB.from_model(request)

            query = insert(RequestDB).values(request_db.dict()).on_conflict_do_update(
                index_elements=[RequestDB.class_id, RequestDB.on_date],
                set_=request_db.dict(),
            )
            await session.execute(query)
            await session.commit()
