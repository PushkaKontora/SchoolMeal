from datetime import date, datetime, time

import freezegun
import pytest

from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import Pupil, PupilID, PupilName
from app.nutrition.domain.request import AlreadyBeenPreparedForSending, Request
from app.nutrition.domain.school_class import ClassID, Literal, Number, SchoolClass
from app.nutrition.domain.times import Day, Period, Timeline, now, yekaterinburg


@freezegun.freeze_time(date(2030, 10, 12))
def test_submitting_to_canteen_for_class(school_class: SchoolClass) -> None:
    not_feeding = _create_pupil(class_id=school_class.id, mealtimes={Mealtime.BREAKFAST}, periods=[])
    period_not_feeding = _create_pupil(class_id=school_class.id, mealtimes={Mealtime.DINNER}, periods=[Day.today()])
    outsider = _create_pupil(class_id=ClassID.generate(), mealtimes={Mealtime.DINNER}, periods=[])
    feeding = _create_pupil(class_id=school_class.id, mealtimes={Mealtime.DINNER}, periods=[])

    request = Request.submit_to_canteen(
        school_class=school_class, pupils=[feeding, outsider, not_feeding, period_not_feeding], on_date=now().date()
    )

    assert request.class_id == school_class.id
    assert request.mealtimes == {Mealtime.DINNER: {feeding.id, outsider.id}}
    assert request.on_date == now().date()
    assert request.created_at == now()


@pytest.mark.parametrize("now_", [time(hour=21), time(hour=21, second=59)])
def test_editing_before_deadline(school_class: SchoolClass, now_: time) -> None:
    with freezegun.freeze_time(datetime.combine(date(2023, 10, 1), now_, tzinfo=yekaterinburg)):
        not_feeding = _create_pupil(class_id=school_class.id, mealtimes=set(), periods=[])
        period_not_feeding = _create_pupil(class_id=school_class.id, mealtimes={Mealtime.DINNER}, periods=[Day.today()])
        feeding = _create_pupil(class_id=school_class.id, mealtimes={Mealtime.DINNER}, periods=[])

        request = Request.submit_to_canteen(
            school_class=school_class, pupils=[feeding, not_feeding, period_not_feeding], on_date=now().date()
        )

        not_feeding.resume_on_mealtime(Mealtime.DINNER)
        feeding.cancel_on_mealtime(Mealtime.DINNER)

        editing = request.edit([not_feeding, feeding, period_not_feeding])

        assert editing.is_ok()
        assert request.mealtimes == {Mealtime.DINNER: {not_feeding.id}}


@pytest.mark.parametrize("now_", [time(hour=22, second=0), time(hour=22, second=1), time(hour=23)])
def test_editing_after_deadline(school_class: SchoolClass, now_: time) -> None:
    with freezegun.freeze_time(datetime.combine(date(2023, 10, 1), now_, tzinfo=yekaterinburg)):
        not_feeding = _create_pupil(class_id=school_class.id, mealtimes=set(), periods=[])

        request = Request.submit_to_canteen(school_class=school_class, pupils=[not_feeding], on_date=now().date())

        not_feeding.resume_on_mealtime(Mealtime.DINNER)

        editing = request.edit([not_feeding])

        assert isinstance(editing.err(), AlreadyBeenPreparedForSending)
        assert request.mealtimes == {Mealtime.DINNER: set()}


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
