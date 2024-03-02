from fastapi import APIRouter, status
from result import Ok, do

from app.gateway.dependencies import NutritionAPIDep
from app.gateway.mobile.dto import CancelPupilForPeriodIn, ResumePupilOnDayIn, UpdateMealtimesIn
from app.shared.fastapi import responses
from app.shared.fastapi.dependencies.headers import AuthorizedUserDep
from app.shared.fastapi.errors import BadRequest
from app.shared.fastapi.schemas import OKSchema


router = APIRouter(prefix="/pupils")


@router.post(
    "/{pupil_id}/resume",
    summary="Поставить ученика на питание на день",
    status_code=status.HTTP_200_OK,
    responses=responses.BAD_REQUEST,
)
async def resume_pupil_on_day(pupil_id: str, body: ResumePupilOnDayIn, nutrition_api: NutritionAPIDep) -> OKSchema:
    return do(
        Ok(OKSchema())
        for _ in await nutrition_api.resume_pupil_on_day(
            pupil_id=pupil_id,
            day=body.day,
        )
    ).unwrap_or_raise(BadRequest)


@router.post(
    "/{pupil_id}/cancel",
    summary="Снять ученика с питания на период",
    status_code=status.HTTP_200_OK,
    responses=responses.BAD_REQUEST,
)
async def cancel_pupil_for_period(
    pupil_id: str, body: CancelPupilForPeriodIn, nutrition_api: NutritionAPIDep
) -> OKSchema:
    return do(
        Ok(OKSchema())
        for _ in await nutrition_api.cancel_pupil_for_period(
            pupil_id=pupil_id,
            start=body.start,
            end=body.end,
        )
    ).unwrap_or_raise(BadRequest)


@router.patch(
    "/{pupil_id}/mealtimes",
    summary="Поставить или снять приёмы пищи у ученика",
    status_code=status.HTTP_200_OK,
    responses=responses.BAD_REQUEST,
)
async def update_mealtimes_at_pupil(pupil_id: str, body: UpdateMealtimesIn, nutrition_api: NutritionAPIDep) -> OKSchema:
    return do(
        Ok(OKSchema())
        for _ in await nutrition_api.update_mealtimes_at_pupil(
            pupil_id=pupil_id,
            breakfast=body.breakfast,
            dinner=body.dinner,
            snacks=body.snacks,
        )
    ).unwrap_or_raise(BadRequest)


@router.post(
    "/{pupil_id}/attach",
    summary="Закрепить ребёнка за родителем",
    status_code=status.HTTP_200_OK,
    responses=responses.BAD_REQUEST,
)
async def attach_pupil_to_parent(
    pupil_id: str, authorized_user: AuthorizedUserDep, nutrition_api: NutritionAPIDep
) -> OKSchema:
    return do(
        Ok(OKSchema())
        for _ in await nutrition_api.attach_pupil_to_parent(
            parent_id=authorized_user.id,
            pupil_id=pupil_id,
        )
    ).unwrap_or_raise(BadRequest)
