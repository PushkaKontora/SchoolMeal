from contextlib import nullcontext
from datetime import datetime, timezone

import freezegun
import pytest

from app.notification.domain.notification import Body, Mark, Notification, Subtitle, Title


@pytest.mark.parametrize(
    ["value", "is_ok"],
    [
        ("", True),
        ("a" * 64, True),
        ("a" * 65, False),
    ],
)
def test_title(value: str, is_ok: bool) -> None:
    with nullcontext() if is_ok else pytest.raises(ValueError):
        title = Title(value)

        assert title.value == value


@pytest.mark.parametrize(
    ["value", "is_ok"],
    [
        ("", True),
        ("a" * 64, True),
        ("a" * 65, False),
    ],
)
def test_subtitle(value: str, is_ok: bool) -> None:
    with nullcontext() if is_ok else pytest.raises(ValueError):
        subtitle = Subtitle(value)

        assert subtitle.value == value


@pytest.mark.parametrize(
    ["value", "is_ok"],
    [
        ("", True),
        ("a" * 3, True),
        ("a" * 4, False),
    ],
)
def test_mark(value: str, is_ok: bool) -> None:
    with nullcontext() if is_ok else pytest.raises(ValueError):
        mark = Mark(value)

        assert mark.value == value


@pytest.mark.parametrize(
    ["value", "is_ok"],
    [
        ("", True),
        ("a" * 255, True),
        ("a" * 256, False),
    ],
)
def test_body(value: str, is_ok: bool) -> None:
    with nullcontext() if is_ok else pytest.raises(ValueError):
        body = Body(value)

        assert body.value == value


@pytest.mark.parametrize(
    ["now_", "expected"],
    [
        (datetime(2024, 5, 31), False),
        (datetime(2024, 6, 1), False),
        (datetime(2024, 6, 2), True),
    ],
)
def test_is_old(notification: Notification, now_: datetime, expected: bool) -> None:
    with freezegun.freeze_time(now_.replace(tzinfo=timezone.utc)):
        assert notification.is_old == expected
