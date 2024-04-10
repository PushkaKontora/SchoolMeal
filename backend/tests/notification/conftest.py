from datetime import datetime, timezone

import pytest

from app.notification.domain.notification import Body, Mark, Notification, NotificationID, Subtitle, Title
from app.notification.domain.user import User
from app.shared.domain.user import UserID


@pytest.fixture
def user() -> User:
    return User(id=UserID.generate(), read_notification_ids=set())


@pytest.fixture
def notification(user: User) -> Notification:
    return Notification(
        id=NotificationID.generate(),
        recipients={user.id},
        title=Title("Караул!!! Скоро диплом"),
        subtitle=Subtitle("Таков путь."),
        mark=Mark("SUS"),
        body=Body("Дорогой дневник. Это последний месяц, который запомнится мне навсегда"),
        created_at=datetime(2024, 4, 1, tzinfo=timezone.utc),
    )


@pytest.fixture
def not_addressed_notification() -> Notification:
    return Notification(
        id=NotificationID.generate(),
        recipients=set(),
        title=Title("Письмо в никуда"),
        subtitle=Subtitle("Всё плохо"),
        mark=Mark("123"),
        body=Body("А просто так"),
        created_at=datetime(2024, 4, 1, tzinfo=timezone.utc),
    )
