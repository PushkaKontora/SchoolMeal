from result import Err, Ok, Result

from app.shared.domain.pupil import PupilID
from app.structure.application.dao.parents import IParentRepository
from app.structure.application.dao.pupils import IPupilRepository
from app.structure.application.errors import NotFoundParent, NotFoundPupil
from app.structure.domain.parent import ParentID
from app.structure.domain.pupil import ParentIsAlreadyAttached


async def attach_pupil_to_parent(
    pupil_id: PupilID, parent_id: ParentID, pupil_repository: IPupilRepository, parent_repository: IParentRepository
) -> Result[None, NotFoundParent | NotFoundPupil | ParentIsAlreadyAttached]:
    if not (pupil := await pupil_repository.get(pupil_id)):
        return Err(NotFoundPupil())

    if not (parent := await parent_repository.get(parent_id)):
        return Err(NotFoundParent())

    attaching = pupil.attach_to_parent(parent)

    if isinstance(attaching, Err):
        return attaching

    await pupil_repository.merge(pupil)

    return Ok(None)
