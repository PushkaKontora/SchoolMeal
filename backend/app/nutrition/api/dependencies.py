from typing import Annotated

from fastapi import Depends

from app.nutrition.application.repositories import IPupilsRepository
from app.nutrition.application.services import NutritionService
from app.nutrition.infrastructure.db.repositories import PupilsRepository
from app.shared.fastapi.dependencies.db import SessionDep


def _get_pupils_repository(session: SessionDep) -> IPupilsRepository:
    return PupilsRepository(session)


def _get_nutrition_service(pupil_repository: IPupilsRepository = Depends(_get_pupils_repository)) -> NutritionService:
    return NutritionService(pupils_repository=pupil_repository)


NutritionServiceDep = Annotated[NutritionService, Depends(_get_nutrition_service)]
