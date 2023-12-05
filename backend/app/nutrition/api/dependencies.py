from typing import Annotated

from fastapi import Depends

from app.nutrition.application.services import NutritionService
from app.nutrition.infrastructure.db.repositories import PupilsRepository
from app.shared.fastapi.dependencies.db import SessionDep
from app.shared.fastapi.dependencies.unit_of_work import UnitOfWorkDep


def _get_nutrition_service(unit_of_work: UnitOfWorkDep, session: SessionDep) -> NutritionService:
    return NutritionService(
        unit_of_work=unit_of_work,
        pupils_repository=PupilsRepository(session),
    )


NutritionServiceDep = Annotated[NutritionService, Depends(_get_nutrition_service)]
