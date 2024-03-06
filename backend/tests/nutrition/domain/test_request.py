from datetime import date, datetime, time

import freezegun
import pytest

from app.nutrition.domain.request import CannotSubmitAfterDeadline, Request, Status
from app.nutrition.domain.school_class import ClassID
from app.nutrition.domain.times import yekaterinburg


@pytest.mark.parametrize("now_", [time(hour=21, tzinfo=yekaterinburg), time(hour=21, second=59, tzinfo=yekaterinburg)])
def test_submitting_manually_to_canteen_before_deadline(now_: time) -> None:
    on_date = date(2023, 10, 1)

    with freezegun.freeze_time(datetime.combine(on_date, now_)):
        request = _create_request(on_date)

        submitting = request.submit_manually()

        assert submitting.is_ok()
        assert submitting.unwrap().status is Status.SUBMITTED


@pytest.mark.parametrize(
    "now_",
    [
        time(hour=22, second=0, tzinfo=yekaterinburg),
        time(hour=22, second=1, tzinfo=yekaterinburg),
        time(hour=23, tzinfo=yekaterinburg),
    ],
)
def test_submitting_manually_to_canteen_after_deadline(now_: time) -> None:
    on_date = date(2023, 10, 1)

    with freezegun.freeze_time(datetime.combine(on_date, now_)):
        request = _create_request(on_date)

        submitting = request.submit_manually()

        assert submitting.is_err()
        assert isinstance(submitting.unwrap_err(), CannotSubmitAfterDeadline)

        assert request.status is Status.PREFILLED


def _create_request(on_date: date) -> Request:
    return Request(class_id=ClassID.generate(), on_date=on_date, mealtimes={}, status=Status.PREFILLED)
