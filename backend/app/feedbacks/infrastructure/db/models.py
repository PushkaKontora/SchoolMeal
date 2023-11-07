from uuid import UUID

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as UUID_DB
from sqlalchemy.orm import Mapped

from app.common.infrastructure.db.base import Base
from app.feedbacks.domain.canteen import Canteen
from app.feedbacks.domain.feedback import Feedback
from app.feedbacks.domain.text import FeedbackText


class CanteenDB(Base):
    __tablename__ = "feedback_canteen"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)

    def to_model(self) -> Canteen:
        return Canteen(id=self.id)

    @classmethod
    def from_model(cls, canteen: Canteen) -> "CanteenDB":
        return cls(id=canteen.id)


class FeedbackDB(Base):
    __tablename__ = "feedback"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)
    canteen_id: Mapped[UUID] = Column(ForeignKey(CanteenDB.id), nullable=False)
    user_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), nullable=False)
    text: Mapped[str] = Column(String(256), nullable=False)

    def to_model(self) -> Feedback:
        return Feedback(
            id=self.id,
            canteen_id=self.canteen_id,
            user_id=self.user_id,
            text=FeedbackText(self.text),
        )

    @classmethod
    def from_model(cls, feedback: Feedback) -> "FeedbackDB":
        return FeedbackDB(
            id=feedback.id,
            canteen_id=feedback.canteen_id,
            user_id=feedback.user_id,
            text=feedback.text.value,
        )
