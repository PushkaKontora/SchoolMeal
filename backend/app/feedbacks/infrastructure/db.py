from uuid import UUID

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.db.base import DictMixin
from app.feedbacks.domain.feedback import Feedback, FeedbackID, FeedbackText, FeedbackType, UserID


class FeedbacksBase(DeclarativeBase, DictMixin):
    metadata = MetaData(schema="feedbacks")


class FeedbackDB(FeedbacksBase):
    __tablename__ = "feedback"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column()
    type: Mapped[int] = mapped_column()
    text: Mapped[str] = mapped_column()

    def __init__(self, id_: UUID, user_id: UUID, type_: int, text: str) -> None:
        super().__init__()

        self.id = id_
        self.user_id = user_id
        self.type = type_
        self.text = text

    def to_model(self) -> Feedback:
        return Feedback(
            id=FeedbackID(self.id),
            user_id=UserID(self.user_id),
            type=FeedbackType(self.type),
            text=FeedbackText(self.text),
        )

    @classmethod
    def from_model(cls, feedback: Feedback) -> "FeedbackDB":
        return FeedbackDB(
            id_=feedback.id.value, type_=feedback.type.value, user_id=feedback.user_id.value, text=feedback.text.value
        )
