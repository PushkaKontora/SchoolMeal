from fastapi import APIRouter, status

from app.common.api import responses
from app.common.api.errors import NotFoundError
from app.nutrition.api.dependencies import PupilsRepositoryDep
from app.nutrition.api.schemas import NutritionOut
from app.nutrition.application import use_cases
from app.nutrition.application.repositories import NotFoundPupil
from app.nutrition.domain.pupil import PupilID


router = APIRouter(tags=["Модуль питания"])


@router.get(
    "/nutrition/{pupil_id}",
    summary="Получить информацию о питании ученика",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def get_pupil_nutrition(pupil_id: str, pupils_repository: PupilsRepositoryDep) -> NutritionOut:
    try:
        pupil = await use_cases.get_pupil(pupil_id=PupilID(pupil_id), pupils_repository=pupils_repository)
    except NotFoundPupil as error:
        raise NotFoundError("Ученик не был найден") from error

    return NutritionOut.from_model(pupil)
