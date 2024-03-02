from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from result import Result

from app.ipc.nutrition.dto import Override


class INutritionAPI(ABC):
    @abstractmethod
    async def resume_pupil_on_day(self, pupil_id: str, day: date) -> Result[None, str]:
        raise NotImplementedError

    @abstractmethod
    async def cancel_pupil_for_period(self, pupil_id: str, start: date, end: date) -> Result[None, str]:
        raise NotImplementedError

    @abstractmethod
    async def update_mealtimes_at_pupil(
        self, pupil_id: str, breakfast: bool | None = None, dinner: bool | None = None, snacks: bool | None = None
    ) -> Result[None, str]:
        raise NotImplementedError

    @abstractmethod
    async def submit_request_to_canteen(
        self, class_id: UUID, on_date: date, overrides: set[Override]
    ) -> Result[None, str]:
        raise NotImplementedError
