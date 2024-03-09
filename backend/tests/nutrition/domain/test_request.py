from datetime import date, datetime, time

import freezegun
import pytest

from app.nutrition.domain.request import CannotSubmitAfterDeadline, Request, RequestStatus
from app.nutrition.domain.time import YEKATERINBURG
from app.shared.domain.school_class import ClassID


@pytest.mark.parametrize("now_", [time(hour=21, tzinfo=YEKATERINBURG), time(hour=21, second=59, tzinfo=YEKATERINBURG)])
def test_submitting_manually_to_canteen_before_deadline(now_: time) -> None:
    on_date = date(2023, 10, 1)

    with freezegun.freeze_time(datetime.combine(on_date, now_)):
        request = _create_request(on_date)

        submitting = request.submit_manually()

        assert submitting.is_ok()
        assert submitting.unwrap().status is RequestStatus.SUBMITTED


@pytest.mark.parametrize(
    "now_",
    [
        time(hour=22, second=0, tzinfo=YEKATERINBURG),
        time(hour=22, second=1, tzinfo=YEKATERINBURG),
        time(hour=23, tzinfo=YEKATERINBURG),
    ],
)
def test_submitting_manually_to_canteen_after_deadline(now_: time) -> None:
    on_date = date(2023, 10, 1)

    with freezegun.freeze_time(datetime.combine(on_date, now_)):
        request = _create_request(on_date)

        submitting = request.submit_manually()

        assert submitting.is_err()
        assert isinstance(submitting.unwrap_err(), CannotSubmitAfterDeadline)

        assert request.status is RequestStatus.PREFILLED


def _create_request(on_date: date) -> Request:
    return Request(
        class_id=ClassID.generate(),
        on_date=on_date,
        mealtimes=set(),
        declarations=set(),
        status=RequestStatus.PREFILLED,
    )
