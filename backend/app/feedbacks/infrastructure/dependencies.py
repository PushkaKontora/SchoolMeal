from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from app.feedbacks.infrastructure.dao.feedback_repository import AlchemyFeedbackRepository


class FeedbacksContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(from_package="app.feedbacks", packages=[".application"], auto_wire=False)

    alchemy = providers.DependenciesContainer()

    feedback_repository = providers.Singleton(AlchemyFeedbackRepository, session_factory=alchemy.session.provider)
