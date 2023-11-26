from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.feedbacks.application.repositories import ICanteenRepository, IFeedbackRepository
from app.feedbacks.domain.feedback import Feedback
from app.feedbacks.infrastructure.db.models import CanteenDB, FeedbackDB


class FeedbackRepository(IFeedbackRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, feedback: Feedback) -> None:
        feedback_db = FeedbackDB.from_model(feedback)

        self._session.add(feedback_db)
        await self._session.flush([feedback_db])


class CanteenRepository(ICanteenRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def exists_by_id(self, canteen_id: UUID) -> bool:
        query = select(1).select_from(CanteenDB).where(CanteenDB.id == canteen_id).limit(1)

        return bool((await self._session.scalars(query)).one_or_none())
