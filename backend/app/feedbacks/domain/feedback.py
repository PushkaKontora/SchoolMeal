from dataclasses import dataclass
from enum import IntEnum, unique
from typing import NewType
from uuid import UUID, uuid4

from result import Ok, Result


UserID = NewType("UserID", UUID)


@dataclass(frozen=True)
class FeedbackID:
    value: UUID

    @classmethod
    def generate(cls) -> "FeedbackID":
        return cls(uuid4())


@unique
class FeedbackType(IntEnum):
    WORK_OF_CANTEEN = 10


@dataclass(frozen=True)
class FeedbackText:
    value: str

    _MAX_LENGTH = 255

    def __post_init__(self) -> None:
        if len(self.value) == 0:
            raise ValueError("Текст не должен быть пустым")

        if len(self.value) > self._MAX_LENGTH:
            raise ValueError(f"Текст отзыва превысил допустимую длину - {self._MAX_LENGTH} символов")


@dataclass
class Feedback:
    id: FeedbackID
    user_id: UserID
    type: FeedbackType
    text: FeedbackText

    @classmethod
    def leave_about_work_of_canteen(cls, user_id: UserID, text: FeedbackText) -> Result["Feedback", None]:
        return Ok(cls(id=FeedbackID.generate(), user_id=user_id, type=FeedbackType.WORK_OF_CANTEEN, text=text))
