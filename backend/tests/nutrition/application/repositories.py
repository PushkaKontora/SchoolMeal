from app.nutrition.application.repositories import IPupilsRepository, NotFoundPupil
from app.nutrition.domain.pupil import Pupil, PupilID


class LocalPupilsRepository(IPupilsRepository):
    def __init__(self, pupils: list[Pupil] | None = None) -> None:
        self._pupil_ids: dict[PupilID, Pupil] = {pupil.id: pupil for pupil in pupils or []}

    async def get_by_id(self, pupil_id: PupilID) -> Pupil:
        try:
            return self._pupil_ids[pupil_id]
        except KeyError as error:
            raise NotFoundPupil from error

    async def update(self, pupil: Pupil) -> None:
        if pupil.id not in self._pupil_ids:
            return

        self._pupil_ids[pupil.id] = pupil
