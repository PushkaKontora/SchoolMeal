from fastapi import APIRouter, status
from result import Err

from app.gateway import responses
from app.gateway.errors import BadRequest, NotFound, UnprocessableEntity
from app.gateway.mobile.pupils.dto import CancelPupilForPeriodBody, ResumePupilOnDayBody, UpdateMealtimesBody
from app.nutrition.api import handlers as nutrition_api
from app.nutrition.api.errors import (
    CannotCancelAfterDeadline,
    CannotResumeAfterDeadline,
    NotFoundParentWithID,
    NotFoundPupilWithID,
    PupilIsAlreadyAttached,
)
from app.shared.api.errors import DomainValidationError
from app.shared.fastapi.dependencies.headers import AuthorizedUserDep
from app.shared.fastapi.schemas import OKSchema


router = APIRouter(prefix="/pupils")


@router.post(
    "/{pupil_id}/resume",
    summary="Поставить ученика на питание на день",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def resume_pupil_on_day(pupil_id: str, body: ResumePupilOnDayBody) -> OKSchema:
    match await nutrition_api.resume_pupil_on_day(pupil_id=pupil_id, day=body.day):
        case Err(NotFoundPupilWithID(message=message)):
            raise NotFound(message)

        case Err(CannotResumeAfterDeadline(message=message)):
            raise BadRequest(message)

    return OKSchema()


@router.post(
    "/{pupil_id}/cancel",
    summary="Снять ученика с питания на период",
    status_code=status.HTTP_200_OK,
    responses=responses.UNPROCESSABLE_ENTITY | responses.NOT_FOUND,
)
async def cancel_pupil_for_period(pupil_id: str, body: CancelPupilForPeriodBody) -> OKSchema:
    match nutrition_api.cancel_pupil_for_period(pupil_id=pupil_id, start=body.start, end=body.end):
        case Err(DomainValidationError(message=message)):
            raise UnprocessableEntity(message)

        case Err(NotFoundPupilWithID(message=message)):
            raise NotFound(message)

        case Err(CannotCancelAfterDeadline(message=message)):
            raise BadRequest(message)

    return OKSchema()


@router.patch(
    "/{pupil_id}/mealtimes",
    summary="Поставить или снять приёмы пищи у ученика",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def update_mealtimes_at_pupil(pupil_id: str, body: UpdateMealtimesBody) -> OKSchema:
    match nutrition_api.update_mealtimes_at_pupil(pupil_id=pupil_id, mealtimes=body.mealtimes):
        case Err(NotFoundPupilWithID(message=message)):
            raise NotFound(message)

    return OKSchema()


@router.post(
    "/{pupil_id}/attach",
    summary="Закрепить ребёнка за родителем",
    status_code=status.HTTP_200_OK,
    responses=responses.BAD_REQUEST,
)
async def attach_pupil_to_parent(pupil_id: str, authorized_user: AuthorizedUserDep) -> OKSchema:
    match nutrition_api.attach_pupil_to_parent(parent_id=authorized_user.id, pupil_id=pupil_id):
        case Err(NotFoundParentWithID(message=message)):
            raise NotFound(message)

        case Err(NotFoundPupilWithID(message=message)):
            raise NotFound(message)

        case Err(PupilIsAlreadyAttached(message=message)):
            raise BadRequest(message)

    return OKSchema()
