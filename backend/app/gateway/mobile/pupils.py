from fastapi import APIRouter, status
from result import Err, as_result

from app.gateway.mobile.dto import CancelForPeriodIn, MealtimeTogglerIn, ResumeOnDayIn
from app.nutrition.application import services
from app.nutrition.application.errors import NotFoundPupil
from app.nutrition.domain.pupil import PupilID
from app.nutrition.domain.times import Day, Period
from app.shared.fastapi import responses
from app.shared.fastapi.errors import NotFound, UnprocessableEntity
from app.shared.fastapi.schemas import OKSchema


router = APIRouter(prefix="/pupils")


@router.post(
    "/{pupil_id}/resume",
    summary="Поставить ученика на питание на день",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def resume_on_day(pupil_id: str, body: ResumeOnDayIn) -> OKSchema:
    id_ = as_result(ValueError)(lambda x: PupilID(x))(pupil_id).unwrap_or_raise(UnprocessableEntity)
    day = as_result(ValueError)(lambda x: Day(x))(body.day).unwrap_or_raise(UnprocessableEntity)

    resuming = await services.resume_on_day(pupil_id=id_, day=day)

    match resuming:
        case Err(NotFoundPupil()):
            raise NotFound(f"Не найден ученик с id={pupil_id}")

    return resuming.map(lambda _: OKSchema()).unwrap()


@router.post(
    "/{pupil_id}/cancel",
    summary="Снять ученика с питания на период",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def cancel_for_period(pupil_id: str, body: CancelForPeriodIn) -> OKSchema:
    id_ = as_result(ValueError)(lambda x: PupilID(x))(pupil_id).unwrap_or_raise(UnprocessableEntity)
    period = as_result(ValueError)(lambda x: Period(start=x[0], end=x[1]))((body.start, body.end)).unwrap_or_raise(
        UnprocessableEntity
    )

    cancelling = await services.cancel_for_period(pupil_id=id_, period=period)

    match cancelling:
        case Err(NotFoundPupil()):
            raise NotFound(f"Не найден ученик с id={pupil_id}")

    return cancelling.map(lambda _: OKSchema()).unwrap()


@router.patch(
    "/{pupil_id}/mealtimes",
    summary="Поставить или снять приёмы пищи у ученика",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def resume_or_cancel_mealtimes_at_pupil(pupil_id: str, togglers: list[MealtimeTogglerIn]) -> OKSchema:
    id_ = as_result(ValueError)(lambda x: PupilID(x))(pupil_id).unwrap_or_raise(UnprocessableEntity)

    if not togglers:
        return OKSchema()

    resuming = await services.resume_or_cancel_mealtimes_at_pupil(
        pupil_id=id_,
        mealtimes={toggler.mealtime: toggler.enabled for toggler in togglers},
    )

    match resuming:
        case Err(NotFoundPupil()):
            raise NotFound(f"Не найден ученик с id={pupil_id}")

    return resuming.map(lambda _: OKSchema()).unwrap()
