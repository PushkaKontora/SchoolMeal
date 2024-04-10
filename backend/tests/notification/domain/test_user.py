from app.notification.domain.notification import Notification
from app.notification.domain.user import User


def test_read_addressed_notification(user: User, notification: Notification) -> None:
    assert user.did_read(notification) is False
    assert user.read(notification) is True
    assert user.did_read(notification) is True


def test_read_not_addressed_notification(user: User, not_addressed_notification: Notification) -> None:
    assert user.did_read(not_addressed_notification) is False
    assert user.read(not_addressed_notification) is False
    assert user.did_read(not_addressed_notification) is False
