from dependency_injector.wiring import Provide

from app.container import Container
from app.db.unit_of_work import UnitOfWork
from app.pupils.db.pupil.filters import ByClassId
from app.pupils.db.pupil.model import Pupil
from app.pupils.domain.entities import PupilOut


async def get_pupils_by_class_id(class_id: int, uow: UnitOfWork = Provide[Container.unit_of_work]) -> list[PupilOut]:
    async with uow:
        pupils = await uow.repository(Pupil).find(ByClassId(class_id))

        return [PupilOut.from_orm(pupil) for pupil in pupils]
