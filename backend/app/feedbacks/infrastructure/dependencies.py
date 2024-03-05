from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from app.feedbacks import api
from app.feedbacks.infrastructure.dao.feedback_repository import AlchemyFeedbackRepository


class FeedbacksContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=[api], auto_wire=False)

    alchemy = providers.DependenciesContainer()

    feedback_repository = providers.Singleton(AlchemyFeedbackRepository, session_factory=alchemy.session.provider)
