from dataclasses import dataclass

from app.feedbacks.application.repositories import ICanteensRepository, IFeedbacksRepository
from app.shared.unit_of_work.abc import Context


@dataclass(frozen=True)
class FeedbacksContext(Context):
    feedbacks: IFeedbacksRepository
    canteens: ICanteensRepository
