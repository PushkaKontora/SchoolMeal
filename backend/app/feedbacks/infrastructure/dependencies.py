from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.feedbacks.infrastructure.api import FeedbacksAPI
from app.feedbacks.infrastructure.dao.feedback_repository import AlchemyFeedbackRepository


class FeedbacksContainer(DeclarativeContainer):
    alchemy = providers.DependenciesContainer()

    feedback_repository = providers.Singleton(AlchemyFeedbackRepository, session_factory=alchemy.session.provider)

    api = providers.Singleton(FeedbacksAPI, feedback_repository=feedback_repository)
