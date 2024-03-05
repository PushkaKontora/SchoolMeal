from pydantic import BaseModel


class LeaveFeedbackAboutCanteenBody(BaseModel):
    text: str
