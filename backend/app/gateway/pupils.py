from datetime import date
from typing import Annotated

from fastapi import APIRouter, Body, Path, status
from result import Err

from app.nutrition.application import commands
from app.nutrition.application.errors import NotFoundPupil
from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import PupilID
from app.nutrition.domain.times import Day, Period
from app.shared.exceptions import DomainException
from app.shared.fastapi import responses
from app.shared.fastapi.errors import NotFoundError, UnprocessableEntityError
from app.shared.fastapi.schemas import OKSchema


router = APIRouter(prefix="/pupils")


@router.post(
    "/{pupil_id}/resume-day",
    summary="Поставить ученика на питание на день",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def resume_on_day(
    pupil_id_dto: Annotated[str, Path(alias="pupil_id")], day_dto: Annotated[date, Body(embed=True, alias="day")]
) -> OKSchema:
    try:
        pupil_id = PupilID(pupil_id_dto)
        day = Day(day_dto)
    except DomainException as error:
        raise UnprocessableEntityError(error.message)

    resuming = await commands.resume_on_day(pupil_id, day)

    match resuming:
        case Err(NotFoundPupil()):
            raise NotFoundError(f"Не найден ученик с id={pupil_id.value}")

    return resuming.map(lambda _: OKSchema()).unwrap()


@router.post(
    "/{pupil_id}/cancel-period",
    summary="Снять ученика с питания на период",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def cancel_for_period(
    pupil_id_dto: Annotated[str, Path(alias="pupil_id")], start: Annotated[date, Body()], end: Annotated[date, Body()]
) -> OKSchema:
    try:
        pupil_id = PupilID(pupil_id_dto)
        period = Period(start, end)
    except DomainException as error:
        raise UnprocessableEntityError(error.message)

    cancelling = await commands.cancel_for_period(pupil_id, period)

    match cancelling:
        case Err(NotFoundPupil()):
            raise NotFoundError(f"Не найден ученик с id={pupil_id.value}")

    return cancelling.map(lambda _: OKSchema()).unwrap()


@router.post(
    "/{pupil_id}/resume-mealtime",
    summary="Поставить ученика на приём пищи",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def resume_on_mealtime(
    pupil_id_dto: Annotated[str, Path(alias="pupil_id")], mealtime: Annotated[Mealtime, Body(embed=True)]
) -> OKSchema:
    try:
        pupil_id = PupilID(pupil_id_dto)
    except DomainException as error:
        raise UnprocessableEntityError(error.message)

    resuming = await commands.resume_on_mealtime(pupil_id, mealtime)

    match resuming:
        case Err(NotFoundPupil()):
            raise NotFoundError(f"Не найден ученик с id={pupil_id.value}")

    return resuming.map(lambda _: OKSchema()).unwrap()


@router.post(
    "/{pupil_id}/cancel-mealtime",
    summary="Снять ученика с приёма пищи",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def cancel_from_mealtime(
    pupil_id_dto: Annotated[str, Path(alias="pupil_id")], mealtime: Annotated[Mealtime, Body(embed=True)]
) -> OKSchema:
    try:
        pupil_id = PupilID(pupil_id_dto)
    except DomainException as error:
        raise UnprocessableEntityError(error.message)

    cancelling = await commands.cancel_from_mealtime(pupil_id, mealtime)

    match cancelling:
        case Err(NotFoundPupil()):
            raise NotFoundError(f"Не найден ученик с id={pupil_id.value}")

    return cancelling.map(lambda _: OKSchema()).unwrap()
