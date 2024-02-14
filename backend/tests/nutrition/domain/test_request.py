from datetime import date, datetime, time

import freezegun
import pytest

from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import Pupil, PupilID, PupilName
from app.nutrition.domain.request import CannotSentRequestAfterDeadline, Request
from app.nutrition.domain.school_class import ClassID, Literal, Number, SchoolClass
from app.nutrition.domain.times import Day, Period, Timeline, now, yekaterinburg


@pytest.mark.parametrize("now_", [time(hour=21, tzinfo=yekaterinburg), time(hour=21, second=59, tzinfo=yekaterinburg)])
def test_submitting_to_canteen_before_deadline(school_class: SchoolClass, now_: time) -> None:
    with freezegun.freeze_time(datetime.combine(date(2023, 10, 1), now_)):
        not_feeding = _create_pupil(class_id=school_class.id, mealtimes={Mealtime.BREAKFAST}, periods=[])
        period_not_feeding = _create_pupil(class_id=school_class.id, mealtimes={Mealtime.DINNER}, periods=[Day.today()])
        outsider = _create_pupil(class_id=ClassID.generate(), mealtimes={Mealtime.DINNER}, periods=[])
        feeding = _create_pupil(class_id=school_class.id, mealtimes={Mealtime.DINNER}, periods=[])

        submitting = Request.submit_to_canteen(
            school_class=school_class,
            pupils=[feeding, outsider, not_feeding, period_not_feeding],
            overrides={},
            on_date=now().date(),
        )
        assert submitting.is_ok()

        request = submitting.unwrap()
        assert request.class_id == school_class.id
        assert request.mealtimes == {Mealtime.DINNER: {feeding.id, outsider.id}}
        assert request.on_date == now().date()
        assert request.created_at == now()


@pytest.mark.parametrize(
    "now_",
    [
        time(hour=22, second=0, tzinfo=yekaterinburg),
        time(hour=22, second=1, tzinfo=yekaterinburg),
        time(hour=23, tzinfo=yekaterinburg),
    ],
)
def test_submitting_to_canteen_after_deadline(school_class: SchoolClass, now_: time) -> None:
    with freezegun.freeze_time(datetime.combine(date(2023, 10, 1), now_)):
        pupil = _create_pupil(class_id=school_class.id, mealtimes={Mealtime.DINNER}, periods=[])

        submitting = Request.submit_to_canteen(
            school_class=school_class, pupils=[pupil], overrides={}, on_date=now().date()
        )
        assert submitting.is_err()

        error = submitting.unwrap_err()
        assert isinstance(error, CannotSentRequestAfterDeadline)
        assert error.deadline == datetime(2023, 10, 1, hour=22, tzinfo=yekaterinburg)


def test_submitting_to_canteen_with_overrides(school_class: SchoolClass) -> None:
    not_feeding = _create_pupil(class_id=school_class.id, mealtimes=set(), periods=[])
    included = _create_pupil(class_id=school_class.id, mealtimes={Mealtime.DINNER}, periods=[])
    excluded = _create_pupil(class_id=school_class.id, mealtimes={Mealtime.DINNER}, periods=[])

    submitting = Request.submit_to_canteen(
        school_class=school_class,
        pupils=[included, excluded, not_feeding],
        overrides={not_feeding.id: set(Mealtime), excluded.id: set()},
        on_date=date(3000, 1, 1),
    )
    assert submitting.is_ok()

    request = submitting.unwrap()
    assert request.mealtimes == {Mealtime.DINNER: {not_feeding.id, included.id}}


@pytest.fixture
def school_class() -> SchoolClass:
    return SchoolClass(
        id=ClassID.generate(),
        teacher_id=None,
        number=Number(11),
        literal=Literal("А"),
        mealtimes={Mealtime.DINNER},
    )


def _create_pupil(class_id: ClassID, mealtimes: set[Mealtime], periods: list[Period]) -> Pupil:
    return Pupil(
        id=PupilID.generate(),
        class_id=class_id,
        last_name=PupilName("Пупкин"),
        first_name=PupilName("Вася"),
        patronymic=None,
        mealtimes=mealtimes,
        preferential_until=None,
        cancellation=Timeline.from_iterable(periods),
    )
