from datetime import date, time
from uuid import UUID

from app.shared.api.errors import APIError


class NotFoundPupilWithID(APIError):
    def __init__(self, pupil_id: str) -> None:
        super().__init__(f"Не найден ученик с id={pupil_id}")


class NotFoundParentWithID(APIError):
    def __init__(self, parent_id: UUID) -> None:
        super().__init__(f"Не найден родитель с id={parent_id}")


class PupilIsAlreadyAttached(APIError):
    def __init__(self) -> None:
        super().__init__("Ребёнок уже привязан к родителю")


class NotFoundSchoolClassWithID(APIError):
    def __init__(self, class_id: UUID) -> None:
        super().__init__(f"Не найден класс с id={class_id}")


class CannotSentRequestAfterDeadline(APIError):
    def __init__(self, on_date: date, after_time: time) -> None:
        super().__init__(f"Невозможно отправить заявку на {on_date} после {after_time.isoformat()}")
