from fastapi import APIRouter, status

from app.common.api import responses
from app.common.api.dependencies.db import SessionDep
from app.common.api.errors import NotFoundError
from app.common.api.schemas import OKSchema
from app.nutrition.api.dependencies import PupilsRepositoryDep
from app.nutrition.api.schemas import MealPlanIn, NutritionOut
from app.nutrition.application import use_cases
from app.nutrition.application.repositories import NotFoundPupil


router = APIRouter(tags=["Модуль питания"])


@router.get(
    "/nutrition/{pupil_id}",
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
    "/nutrition/{pupil_id}/plan",
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
