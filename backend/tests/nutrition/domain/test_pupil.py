import re

from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import Pupil, PupilID
from app.nutrition.domain.times import Day, now


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
