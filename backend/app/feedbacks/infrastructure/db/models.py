from uuid import UUID

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as UUID_DB
from sqlalchemy.orm import Mapped, declarative_base

from app.db.base import Base
from app.feedbacks.domain.canteen import Canteen
from app.feedbacks.domain.feedback import Feedback
from app.feedbacks.domain.text import FeedbackText


FeedbacksBase = declarative_base(cls=Base)
FeedbacksBase.__table_args__ = {"schema": "feedbacks"}


class CanteenDB(FeedbacksBase):
    __tablename__ = "canteen"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)

    def __init__(self, id_: UUID) -> None:
        super().__init__()

        self.id = id_

    def to_model(self) -> Canteen:
        return Canteen(id=self.id)

    @classmethod
    def from_model(cls, canteen: Canteen) -> "CanteenDB":
        return cls(id_=canteen.id)


class FeedbackDB(FeedbacksBase):
    __tablename__ = "feedback"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)
    canteen_id: Mapped[UUID] = Column(ForeignKey(CanteenDB.id), nullable=False)
    user_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), nullable=False)
    text: Mapped[str] = Column(String(256), nullable=False)

    def __init__(self, id_: UUID, canteen_id: UUID, user_id: UUID, text: str) -> None:
        super().__init__()

        self.id = id_
        self.canteen_id = canteen_id
        self.user_id = user_id
        self.text = text

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
            id_=feedback.id,
            canteen_id=feedback.canteen_id,
            user_id=feedback.user_id,
            text=feedback.text.value,
        )
