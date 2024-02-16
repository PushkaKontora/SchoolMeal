from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from sqlalchemy.ext.asyncio import AsyncSession

from app.feedbacks import application
from app.feedbacks.infrastructure.dao import AlchemyFeedbackRepository


class FeedbacksContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=[application])

    session = providers.Dependency(instance_of=AsyncSession)

    feedback_repository = providers.Singleton(AlchemyFeedbackRepository, session_factory=session.provider)
