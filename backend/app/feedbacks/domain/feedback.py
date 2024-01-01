from uuid import UUID

from pydantic.dataclasses import dataclass

from app.feedbacks.domain.text import FeedbackText
from app.shared.domain import Entity


@dataclass
class Feedback(Entity):
    id: UUID
    canteen_id: UUID
    user_id: UUID
    text: FeedbackText
