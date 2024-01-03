from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Dependency, Factory
from sqlalchemy.ext.asyncio import AsyncSession

from app.feedbacks import api, application
from app.feedbacks.application.services import FeedbacksService
from app.feedbacks.application.unit_of_work import FeedbacksContext
from app.feedbacks.infrastructure.db.repositories import CanteensRepository, FeedbacksRepository
from app.shared.unit_of_work.alchemy import AlchemyUnitOfWork


class FeedbacksContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=[api, application])

    session = Dependency(instance_of=AsyncSession)

    unit_of_work = Factory(
        AlchemyUnitOfWork,
        session_factory=session.provider,
        context_factory=lambda session: FeedbacksContext(
            feedbacks=FeedbacksRepository(session),
            canteens=CanteensRepository(session),
        ),
    )

    service = Factory(FeedbacksService, unit_of_work=unit_of_work)
