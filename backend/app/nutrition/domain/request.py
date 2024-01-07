from datetime import date, datetime
from enum import IntEnum, unique
from uuid import UUID

from pydantic.dataclasses import dataclass

from app.nutrition.domain.pupil import PupilID
from app.shared.domain.abc import Entity, ValueObject
from app.shared.domain.money import Money


class RequestAlreadySubmitted(Exception):
    def __init__(self, id_: UUID) -> None:
        self.id = id_


@unique
class RequestStatus(IntEnum):
    PREPARED = 0
    SUBMITTED = 1


@dataclass(frozen=True, eq=True)
class PupilInfo(ValueObject):
    pupil_id: PupilID
    breakfast: bool
    dinner: bool
    snacks: bool
    preferential: bool
    debit: Money


@dataclass
class Request(Entity):
    id: UUID
    status: RequestStatus
    class_id: UUID
    pupils: list[PupilInfo]
    on_date: date
    created_at: datetime

    def submit(self) -> None:
        """
        :raise RequestAlreadySubmitted: заявка уже отправлена
        """

        if self.status is RequestStatus.SUBMITTED:
            raise RequestAlreadySubmitted(id_=self.id)

        self.status = RequestStatus.SUBMITTED
