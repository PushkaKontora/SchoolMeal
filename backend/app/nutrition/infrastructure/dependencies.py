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
from app.nutrition.application.queries.menus.get_menu_on_date import GetMenuOnDateQueryExecutor
from app.nutrition.application.queries.pupils.get_pupil_by_id import GetPupilByIDQueryExecutor
from app.nutrition.application.queries.pupils.get_pupils import GetPupilsQueryExecutor
from app.nutrition.application.queries.school_classes.get_school_class_by_id import GetSchoolClassByIDQueryExecutor
from app.nutrition.application.queries.school_classes.get_school_classes import GetSchoolClassesQueryExecutor
from app.nutrition.infrastructure.db.repositories import (
    AlchemyMenusRepository,
    AlchemyParentsRepository,
    AlchemyPupilsRepository,
    AlchemySchoolClassesRepository,
)
from app.shared.objects_storage.local import LocalObjectsStorage, Protocol
from app.shared.unit_of_work.alchemy import AlchemyUnitOfWork


class NutritionContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=[api, commands])

    object_storage_config = Configuration(strict=True)

    session = Dependency(instance_of=AsyncSession)

    unit_of_work = Factory(
        AlchemyUnitOfWork,
        session_factory=session.provider,
        context_factory=lambda session: NutritionContext(
            pupils=AlchemyPupilsRepository(session),
            parents=AlchemyParentsRepository(session),
            menus=AlchemyMenusRepository(session),
            school_classes=AlchemySchoolClassesRepository(session),
        ),
    )

    objects_storage = Singleton(
        LocalObjectsStorage,
        protocol=Factory(Protocol, object_storage_config.protocol),
        host=object_storage_config.host,
        port=object_storage_config.port,
        base_path=Factory(Path, object_storage_config.base_path),
    )

    attach_child_to_parent_command_handler = Factory(AttachChildToParentCommandHandler, unit_of_work=unit_of_work)
    cancel_nutrition_command_handler = Factory(CancelNutritionCommandHandler, unit_of_work=unit_of_work)
    change_plan_command_handler = Factory(UpdateMealtimesCommandHandler, unit_of_work=unit_of_work)
    resume_nutrition_command_handler = Factory(ResumeNutritionCommandHandler, unit_of_work=unit_of_work)

    get_children_query_executor = Factory(GetChildrenQueryExecutor, session_factory=session.provider)
    get_pupil_by_id_executor = Factory(GetPupilByIDQueryExecutor, unit_of_work=unit_of_work)
    get_pupils = Factory(GetPupilsQueryExecutor, unit_of_work=unit_of_work)
    get_school_classes_executor = Factory(GetSchoolClassesQueryExecutor, unit_of_work=unit_of_work)
    get_school_class_by_id_executor = Factory(GetSchoolClassByIDQueryExecutor, unit_of_work=unit_of_work)
    get_menus_query_executor = Factory(
        GetMenuOnDateQueryExecutor, unit_of_work=unit_of_work, objects_storage=objects_storage
    )
