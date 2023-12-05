from datetime import date
from typing import Annotated

from fastapi import APIRouter, Body, status

from app.nutrition.api.dependencies import NutritionServiceDep
from app.nutrition.api.schemas import CancellationPeriodIn, CancellationPeriodOut, MealPlanIn, NutritionOut
from app.nutrition.application.repositories import NotFoundPupil
from app.nutrition.domain.periods import (
    EndCannotBeGreaterThanStart,
    ExceededMaxLengthReason,
    SpecifiedReasonCannotBeEmpty,
)
from app.shared.fastapi import responses
from app.shared.fastapi.errors import BadRequestError, NotFoundError
from app.shared.fastapi.schemas import OKSchema


router = APIRouter(prefix="/nutrition/{pupil_id}", tags=["Питание"])


@router.get(
    "",
    summary="Получить информацию о питании ученика",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def get_pupil_nutrition(pupil_id: str, nutrition_service: NutritionServiceDep) -> NutritionOut:
    try:
        pupil = await nutrition_service.get_pupil(pupil_id=pupil_id)
    except NotFoundPupil as error:
        raise NotFoundError("Ученик не был найден") from error

    return NutritionOut.from_model(pupil)


@router.put(
    "/plan",
    summary="Изменить план приёма пищи",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def change_meal_plan_for_pupil(
    pupil_id: str, plan: MealPlanIn, nutrition_service: NutritionServiceDep
) -> OKSchema:
    try:
        await nutrition_service.change_meal_plan_for_pupil(
            pupil_id=pupil_id,
            has_breakfast=plan.has_breakfast,
            has_dinner=plan.has_dinner,
            has_snacks=plan.has_snacks,
        )

    except NotFoundPupil as error:
        raise NotFoundError("Ученик не найден") from error

    return OKSchema()


@router.post(
    "/cancel",
    summary="Снять ребёнка с питания на период",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND | responses.BAD_REQUEST,
)
async def cancel_pupil_nutrition_for_period(
    pupil_id: str, period_in: CancellationPeriodIn, nutrition_service: NutritionServiceDep
) -> list[CancellationPeriodOut]:
    try:
        periods = await nutrition_service.cancel_pupil_nutrition_for_period(
            pupil_id=pupil_id,
            starts_at=period_in.starts_at,
            ends_at=period_in.ends_at,
            reason=period_in.reason,
        )

    except NotFoundPupil as error:
        raise NotFoundError("Ученик не найден") from error

    except SpecifiedReasonCannotBeEmpty as error:
        raise BadRequestError("Текст указанной причины должен содержать хотя бы один символ") from error

    except ExceededMaxLengthReason as error:
        raise BadRequestError("Превышена максимальная длина причины") from error

    except EndCannotBeGreaterThanStart as error:
        raise BadRequestError("Дата начала периода больше, чем конечная дата") from error

    return [CancellationPeriodOut.from_model(period) for period in periods]


@router.post(
    "/resume",
    summary="Поставить ребёнка на питание в дату",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND | responses.BAD_REQUEST,
)
async def resume_pupil_nutrition_on_day(
    pupil_id: str,
    date_in: Annotated[date, Body(embed=True, alias="date")],
    nutrition_service: NutritionServiceDep,
) -> list[CancellationPeriodOut]:
    try:
        periods = await nutrition_service.resume_pupil_nutrition_on_day(pupil_id=pupil_id, date_=date_in)

    except NotFoundPupil as error:
        raise NotFoundError("Ученик не найден") from error

    return [CancellationPeriodOut.from_model(period) for period in periods]
