from fastapi import APIRouter, status
from result import Err

from app.gateway.mobile.dto import CancelForPeriodIn, MealtimeTogglerIn, ResumeOnDayIn
from app.nutrition.application import commands
from app.nutrition.application.errors import NotFoundPupil
from app.nutrition.domain.pupil import PupilID
from app.nutrition.domain.times import Day, Period
from app.shared.exceptions import DomainException
from app.shared.fastapi import responses
from app.shared.fastapi.errors import NotFoundError, UnprocessableEntityError
from app.shared.fastapi.schemas import OKSchema


router = APIRouter(prefix="/pupils")


@router.post(
    "/{pupil_id}/resume",
    summary="Поставить ученика на питание на день",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def resume_on_day(pupil_id: str, body: ResumeOnDayIn) -> OKSchema:
    try:
        pupil_id_ = PupilID(pupil_id)
        day = Day(body.day)
    except DomainException as error:
        raise UnprocessableEntityError(error.message)

    resuming = await commands.resume_on_day(pupil_id=pupil_id_, day=day)

    match resuming:
        case Err(NotFoundPupil()):
            raise NotFoundError(f"Не найден ученик с id={pupil_id}")

    return resuming.map(lambda _: OKSchema()).unwrap()


@router.post(
    "/{pupil_id}/cancel",
    summary="Снять ученика с питания на период",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def cancel_for_period(pupil_id: str, body: CancelForPeriodIn) -> OKSchema:
    try:
        pupil_id_ = PupilID(pupil_id)
        period = Period(start=body.start, end=body.end)
    except DomainException as error:
        raise UnprocessableEntityError(error.message)

    cancelling = await commands.cancel_for_period(pupil_id_, period)

    match cancelling:
        case Err(NotFoundPupil()):
            raise NotFoundError(f"Не найден ученик с id={pupil_id}")

    return cancelling.map(lambda _: OKSchema()).unwrap()


@router.patch(
    "/{pupil_id}/mealtimes",
    summary="Поставить или снять приёмы пищи у ученика",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def resume_or_cancel_mealtimes_at_pupil(pupil_id: str, togglers: list[MealtimeTogglerIn]) -> OKSchema:
    try:
        pupil_id_ = PupilID(pupil_id)
    except DomainException as error:
        raise UnprocessableEntityError(error.message)

    if not togglers:
        return OKSchema()

    resuming = await commands.resume_or_cancel_mealtimes_at_pupil(
        pupil_id=pupil_id_,
        mealtimes={toggler.mealtime: toggler.enabled for toggler in togglers},
    )

    match resuming:
        case Err(NotFoundPupil()):
            raise NotFoundError(f"Не найден ученик с id={pupil_id}")

    return resuming.map(lambda _: OKSchema()).unwrap()
