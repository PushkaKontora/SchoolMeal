from uuid import UUID

from dependency_injector.wiring import Provide, inject
from result import Err, Ok, Result

from app.shared.domain.pupil import PupilID
from app.structure.api import errors
from app.structure.application import services
from app.structure.application.dao.parents import IParentRepository
from app.structure.application.dao.pupils import IPupilRepository
from app.structure.application.errors import NotFoundParent, NotFoundPupil
from app.structure.domain.parent import ParentID
from app.structure.domain.pupil import ParentIsAlreadyAttached
from app.structure.infrastructure.dependencies import StructureContainer


@inject
async def attach_pupil_to_parent(
    pupil_id: str,
    parent_id: UUID,
    pupil_repository: IPupilRepository = Provide[StructureContainer.pupil_repository],
    parent_repository: IParentRepository = Provide[StructureContainer.parent_repository],
) -> Result[None, errors.NotFoundPupilWithID | errors.NotFoundParentWithID | errors.PupilIsAlreadyAttached]:
    match await services.attach_pupil_to_parent(
        pupil_id=PupilID(pupil_id),
        parent_id=ParentID(parent_id),
        pupil_repository=pupil_repository,
        parent_repository=parent_repository,
    ):
        case Err(NotFoundPupil()):
            return Err(errors.NotFoundPupilWithID(pupil_id))

        case Err(NotFoundParent()):
            return Err(errors.NotFoundParentWithID(parent_id))

        case Err(ParentIsAlreadyAttached()):
            return Err(errors.PupilIsAlreadyAttached())

    return Ok(None)
