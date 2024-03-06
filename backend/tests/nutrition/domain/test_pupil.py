import re
from datetime import date, datetime, time

import freezegun
import pytest

from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import CannotCancelAfterDeadline, CannotResumeAfterDeadline, Pupil, PupilID
from app.nutrition.domain.time import Day, Period, now, yekaterinburg


def test_generating_id() -> None:
    regex = re.compile(r"[a-z\d]{20}")

    for _ in range(1000):
        pupil_id = PupilID.generate().value

        assert regex.fullmatch(pupil_id), pupil_id


def test_cancelling_mealtime_where_pupil_eats(pupil: Pupil) -> None:
    pupil.cancel_from_mealtime(Mealtime.DINNER)

    assert not pupil.mealtimes


def test_cancelling_mealtime_where_pupil_does_not_eat(pupil: Pupil) -> None:
    pupil.cancel_from_mealtime(Mealtime.BREAKFAST)

    assert pupil.mealtimes == {Mealtime.DINNER}


@pytest.mark.parametrize(
    ["now_", "deadline"],
    [
        (datetime(2023, 1, 1), None),
        (datetime(2023, 1, 2, hour=21, minute=59), None),
        (datetime(2023, 1, 2, hour=22, minute=0), datetime(2023, 1, 2, hour=22, minute=0)),
        (datetime(2023, 1, 2, hour=22, minute=1), datetime(2023, 1, 2, hour=22, minute=0)),
        (datetime(2023, 3, 10), datetime(2023, 1, 2, hour=22, minute=0)),
        (datetime(2023, 5, 5), datetime(2023, 1, 2, hour=22, minute=0)),
        (datetime(2023, 5, 6), datetime(2023, 1, 2, hour=22, minute=0)),
    ],
)
def test_cancelling_for_period(pupil: Pupil, now_: datetime, deadline: datetime | None) -> None:
    period = Period(start=date(2023, 1, 2), end=date(2023, 5, 5))

    with freezegun.freeze_time(now_.astimezone(yekaterinburg)):
        cancelling = pupil.cancel_for_period(period)

        if not deadline:
            assert cancelling.is_ok()
            return

        assert cancelling.is_err()

        error = cancelling.unwrap_err()
        assert isinstance(error, CannotCancelAfterDeadline)
        assert error.deadline == deadline.astimezone(yekaterinburg)


@pytest.mark.parametrize(
    ["now_", "has_deadline_come"],
    [
        (datetime(2023, 1, 1), False),
        (datetime(2023, 1, 2, hour=21, minute=59), False),
        (datetime(2023, 1, 2, hour=22, minute=0), True),
        (datetime(2023, 1, 2, hour=22, minute=1), True),
        (datetime(2023, 1, 3), True),
    ],
)
def test_resuming_on_day(pupil: Pupil, now_: datetime, has_deadline_come: bool) -> None:
    now_in_yekaterinburg = now_.astimezone(yekaterinburg)

    day = Day(date(2023, 1, 2))

    with freezegun.freeze_time(now_in_yekaterinburg):
        resuming = pupil.resume_on_day(day)

        if not has_deadline_come:
            assert resuming.is_ok()
            return

        assert resuming.is_err()

        error = resuming.unwrap_err()
        assert isinstance(error, CannotResumeAfterDeadline)
        assert error.deadline == datetime.combine(day.value, time(hour=22, tzinfo=yekaterinburg))


def test_resuming_mealtime_where_pupil_does_not_eat(pupil: Pupil) -> None:
    pupil.resume_on_mealtime(Mealtime.BREAKFAST)

    assert pupil.mealtimes == {Mealtime.DINNER, Mealtime.BREAKFAST}


def test_resuming_mealtime_where_pupil_eats(pupil: Pupil) -> None:
    pupil.resume_on_mealtime(Mealtime.DINNER)

    assert pupil.mealtimes == {Mealtime.DINNER}


def test_pupil_does_not_eat_when_mealtime_is_cancelled(pupil: Pupil) -> None:
    eating = pupil.cancel_from_mealtime(Mealtime.DINNER).and_then(
        lambda x: x.does_eat(day=Day(now().date()), mealtime=Mealtime.DINNER)
    )

    assert not eating


def test_pupil_does_not_eat_when_pupil_is_cancelled_for_period(pupil: Pupil) -> None:
    today = Day.today()

    eating = pupil.cancel_for_period(today).and_then(lambda x: x.does_eat(day=today, mealtime=Mealtime.DINNER))

    assert not eating


def test_pupil_eats(pupil: Pupil) -> None:
    eating = pupil.does_eat(day=Day.today(), mealtime=Mealtime.DINNER)

    assert eating
