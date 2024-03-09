from uuid import UUID

from app.shared.api.errors import APIError


class NotFoundPupilWithID(APIError):
    def __init__(self, pupil_id: str) -> None:
        super().__init__(message=f"Не найден ученик с id={pupil_id}")


class NotFoundParentWithID(APIError):
    def __init__(self, parent_id: UUID) -> None:
        super().__init__(message=f"Не найден родитель с id={parent_id}")


class PupilIsAlreadyAttached(APIError):
    def __init__(self) -> None:
        super().__init__(message="Ребёнок уже привязан к родителю")
