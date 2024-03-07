from typing import AsyncContextManager, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.feedbacks.application.dao.feedbacks import IFeedbackRepository
from app.feedbacks.domain.feedback import Feedback
from app.feedbacks.infrastructure.db import FeedbackDB


class AlchemyFeedbackRepository(IFeedbackRepository):
    def __init__(self, session_factory: Callable[[], AsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def add(self, feedback: Feedback) -> None:
        async with self._session_factory() as session:
            feedback_db = FeedbackDB.from_model(feedback)

            session.add(feedback_db)
            await session.commit()
