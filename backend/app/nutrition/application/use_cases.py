from app.nutrition.application.repositories import IPupilsRepository
from app.nutrition.domain.pupil import Pupil, PupilID


async def get_pupil(pupil_id: PupilID, pupils_repository: IPupilsRepository) -> Pupil:
    """
    :raise NotFoundPupil:
    """
    return await pupils_repository.get_by_id(pupil_id)
