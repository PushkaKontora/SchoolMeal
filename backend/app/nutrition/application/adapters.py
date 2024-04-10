from abc import ABC, abstractmethod

from app.nutrition.domain.teacher import TeacherID


class INotificationAdapter(ABC):
    @abstractmethod
    async def notify_teacher_about_cancellation(
        self, teacher_id: TeacherID, title: str, subtitle: str, mark: str, body: str
    ) -> None:
        raise NotImplementedError
