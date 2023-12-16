from typing import Annotated

from fastapi import Depends

from app.feedbacks.application.services import FeedbacksService
from app.feedbacks.application.unit_of_work import FeedbacksContext
from app.feedbacks.infrastructure.db.repositories import CanteensRepository, FeedbacksRepository
from app.shared.db.session import get_session_cls
from app.shared.fastapi.dependencies.settings import DatabaseSettingsDep
from app.shared.unit_of_work.alchemy import AlchemyUnitOfWork


def _get_feedbacks_service(database_settings: DatabaseSettingsDep) -> FeedbacksService:
    return FeedbacksService(
        unit_of_work=AlchemyUnitOfWork(
            session_factory=get_session_cls(settings=database_settings),
            context_factory=lambda session: FeedbacksContext(
                feedbacks=FeedbacksRepository(session),
                canteens=CanteensRepository(session),
            ),
        )
    )


FeedbacksServiceDep = Annotated[FeedbacksService, Depends(_get_feedbacks_service)]
