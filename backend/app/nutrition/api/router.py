from fastapi import APIRouter, status

from app.common.api import responses
from app.common.api.dependencies.db import SessionDep
from app.common.api.errors import BadRequestError, NotFoundError
from app.common.api.schemas import OKSchema
from app.nutrition.api.dependencies import PupilsRepositoryDep
from app.nutrition.api.schemas import CancellationPeriodIn, CancellationPeriodOut, MealPlanIn, NutritionOut
from app.nutrition.application import use_cases
from app.nutrition.application.repositories import NotFoundPupil
from app.nutrition.domain.periods import (
    EndCannotBeGreaterThanStart,
    ExceededMaxLengthReason,
    SpecifiedReasonCannotBeEmpty,
)


router = APIRouter(prefix="/nutrition/{pupil_id}", tags=["Питание"])


@router.get(
    "",
    summary="Получить информацию о питании ученика",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def get_pupil_nutrition(pupil_id: str, pupils_repository: PupilsRepositoryDep) -> NutritionOut:
    try:
        pupil = await use_cases.get_pupil(pupil_id=pupil_id, pupils_repository=pupils_repository)
    except NotFoundPupil as error:
        raise NotFoundError("Ученик не был найден") from error

    return NutritionOut.from_model(pupil)


@router.put(
    "/plan",
    summary="Изменить план приёма пищи",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def update_meal_plan_for_pupil(
    pupil_id: str, plan: MealPlanIn, session: SessionDep, pupils_repository: PupilsRepositoryDep
) -> OKSchema:
    try:
        async with session.begin():
            await use_cases.make_meal_plan_for_pupil(
                pupil_id=pupil_id,
                has_breakfast=plan.has_breakfast,
                has_dinner=plan.has_dinner,
                has_snacks=plan.has_snacks,
                pupils_repository=pupils_repository,
            )
            await session.commit()

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
    pupil_id: str, period_in: CancellationPeriodIn, session: SessionDep, pupils_repository: PupilsRepositoryDep
) -> list[CancellationPeriodOut]:
    try:
        async with session.begin():
            periods = await use_cases.cancel_pupil_nutrition_for_period(
                pupil_id=pupil_id,
                starts_at=period_in.starts_at,
                ends_at=period_in.ends_at,
                reason=period_in.reason,
                pupils_repository=pupils_repository,
            )

            await session.commit()

    except NotFoundPupil as error:
        raise NotFoundError("Ученик не найден") from error

    except SpecifiedReasonCannotBeEmpty as error:
        raise BadRequestError("Текст указанной причины должен содержать хотя бы один символ") from error

    except ExceededMaxLengthReason as error:
        raise BadRequestError("Превышена максимальная длина причины") from error

    except EndCannotBeGreaterThanStart as error:
        raise BadRequestError("Дата начала периода больше, чем конечная дата") from error

    return [CancellationPeriodOut.from_model(period) for period in periods]
