from pydantic.dataclasses import dataclass

from app.shared.domain import ValueObject


class InsufficientMinLengthFeedbackText(Exception):
    pass


class ExceededMaxLengthFeedbackText(Exception):
    pass


@dataclass(eq=True, frozen=True)
class FeedbackText(ValueObject):
    value: str

    def __post_init_post_parse__(self) -> None:
        if len(self.value) == 0:
            raise InsufficientMinLengthFeedbackText

        if len(self.value) > 255:
            raise ExceededMaxLengthFeedbackText
