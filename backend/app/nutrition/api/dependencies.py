from typing import Annotated

from fastapi import Depends

from app.nutrition.application.services import NutritionService
from app.nutrition.application.unit_of_work import NutritionContext
from app.nutrition.infrastructure.db.repositories import PupilsRepository
from app.shared.db.session import get_session_cls
from app.shared.fastapi.dependencies.settings import DatabaseSettingsDep
from app.shared.unit_of_work.alchemy import AlchemyUnitOfWork


def _get_nutrition_service(database_settings: DatabaseSettingsDep) -> NutritionService:
    return NutritionService(
        unit_of_work=AlchemyUnitOfWork(
            session_factory=get_session_cls(settings=database_settings),
            context_factory=lambda session: NutritionContext(
                pupils=PupilsRepository(session),
            ),
        )
    )


NutritionServiceDep = Annotated[NutritionService, Depends(_get_nutrition_service)]
