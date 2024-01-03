from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Dependency, Factory
from sqlalchemy.ext.asyncio import AsyncSession

from app.nutrition import api, commands
from app.nutrition.commands.attach_child_to_parent import AttachChildToParentCommandHandler
from app.nutrition.commands.cancel_nutrition import CancelNutritionCommandHandler
from app.nutrition.commands.context import NutritionContext
from app.nutrition.commands.resume_nutrition import ResumeNutritionCommandHandler
from app.nutrition.commands.update_mealtimes import UpdateMealtimesCommandHandler
from app.nutrition.infrastructure.db.repositories import AlchemyParentsRepository, AlchemyPupilsRepository
from app.nutrition.queries.get_children import GetChildrenQueryExecutor
from app.nutrition.queries.get_nutrition_info import GetNutritionInfoQueryExecutor
from app.shared.unit_of_work.alchemy import AlchemyUnitOfWork


class NutritionContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=[api, commands])

    session = Dependency(instance_of=AsyncSession)

    pupils_repository = Factory(AlchemyPupilsRepository, session=session)

    unit_of_work = Factory(
        AlchemyUnitOfWork,
        session_factory=session.provider,
        context_factory=lambda session: NutritionContext(
            pupils=AlchemyPupilsRepository(session),
            parents=AlchemyParentsRepository(session),
        ),
    )

    attach_child_to_parent_command_handler = Factory(AttachChildToParentCommandHandler, unit_of_work=unit_of_work)
    cancel_nutrition_command_handler = Factory(CancelNutritionCommandHandler, unit_of_work=unit_of_work)
    change_plan_command_handler = Factory(UpdateMealtimesCommandHandler, unit_of_work=unit_of_work)
    resume_nutrition_command_handler = Factory(ResumeNutritionCommandHandler, unit_of_work=unit_of_work)

    get_children_query_executor = Factory(GetChildrenQueryExecutor, session_factory=session.provider)
    get_nutrition_info_executor = Factory(GetNutritionInfoQueryExecutor, pupils_repository=pupils_repository)
