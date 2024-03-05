from uuid import UUID

from pydantic import BaseModel


class LeaveFeedbackAboutCanteenIn(BaseModel):
    user_id: UUID
    text: str
