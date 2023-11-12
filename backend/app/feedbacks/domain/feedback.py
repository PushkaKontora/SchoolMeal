from uuid import UUID

from pydantic import BaseModel

from app.feedbacks.domain.text import FeedbackText


class Feedback(BaseModel):
    id: UUID
    canteen_id: UUID
    user_id: UUID
    text: FeedbackText
