from pathlib import Path

from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration, Dependency, Factory, Singleton
from sqlalchemy.ext.asyncio import AsyncSession

from app.nutrition import api
from app.nutrition.application import commands
from app.nutrition.application.commands.attach_child_to_parent import AttachChildToParentCommandHandler
from app.nutrition.application.commands.cancel_nutrition import CancelNutritionCommandHandler
from app.nutrition.application.commands.resume_nutrition import ResumeNutritionCommandHandler
from app.nutrition.application.commands.update_mealtimes import UpdateMealtimesCommandHandler
from app.nutrition.application.context import NutritionContext
from app.nutrition.application.queries.get_children import GetChildrenQueryExecutor
from app.nutrition.application.queries.get_menus import GetMenusQueryExecutor
from app.nutrition.application.queries.get_nutrition_info import GetNutritionInfoQueryExecutor
from app.nutrition.application.queries.get_school_classes import GetSchoolClassesQueryExecutor
from app.nutrition.infrastructure.db.repositories import (
    AlchemyMenusRepository,
    AlchemyParentsRepository,
    AlchemyPupilsRepository,
)
from app.shared.objects_storage.local import LocalObjectsStorage, Protocol
from app.shared.unit_of_work.alchemy import AlchemyUnitOfWork


class NutritionContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=[api, commands])

    gateway_config = Configuration(strict=True)

    session = Dependency(instance_of=AsyncSession)

    pupils_repository = Factory(AlchemyPupilsRepository, session=session)

    unit_of_work = Factory(
        AlchemyUnitOfWork,
        session_factory=session.provider,
        context_factory=lambda session: NutritionContext(
            pupils=AlchemyPupilsRepository(session),
            parents=AlchemyParentsRepository(session),
            menus=AlchemyMenusRepository(session),
        ),
    )

    objects_storage = Singleton(
        LocalObjectsStorage,
        protocol=Factory(Protocol, gateway_config.protocol),
        host=gateway_config.host,
        port=gateway_config.port,
        base_path=Factory(Path, gateway_config.base_path),
    )

    attach_child_to_parent_command_handler = Factory(AttachChildToParentCommandHandler, unit_of_work=unit_of_work)
    cancel_nutrition_command_handler = Factory(CancelNutritionCommandHandler, unit_of_work=unit_of_work)
    change_plan_command_handler = Factory(UpdateMealtimesCommandHandler, unit_of_work=unit_of_work)
    resume_nutrition_command_handler = Factory(ResumeNutritionCommandHandler, unit_of_work=unit_of_work)

    get_children_query_executor = Factory(GetChildrenQueryExecutor, session_factory=session.provider)
    get_nutrition_info_executor = Factory(GetNutritionInfoQueryExecutor, pupils_repository=pupils_repository)
    get_school_classes_executor = Factory(GetSchoolClassesQueryExecutor, session_factory=session.provider)
    get_menus_query_executor = Factory(
        GetMenusQueryExecutor, unit_of_work=unit_of_work, objects_storage=objects_storage
    )
