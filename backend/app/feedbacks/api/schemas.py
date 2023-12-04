from app.shared.fastapi.schemas import FrontendModel


class FeedbackIn(FrontendModel):
    text: str
