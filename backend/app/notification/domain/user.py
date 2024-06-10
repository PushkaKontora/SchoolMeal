from dataclasses import dataclass

from app.notification.domain.notification import Notification, NotificationID
from app.shared.domain.user import UserID


@dataclass
class User:
    id: UserID
    read_notification_ids: set[NotificationID]

    def read(self, notification: Notification) -> bool:
        if self.id not in notification.recipients:
            return False

        self.read_notification_ids.add(notification.id)

        return True

    def did_read(self, notification: Notification) -> bool:
        return notification.id in self.read_notification_ids

    def is_recipient(self, notification: Notification) -> bool:
        return self.id in notification.recipients
