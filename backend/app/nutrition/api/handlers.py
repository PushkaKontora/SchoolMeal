from datetime import date
from uuid import UUID

from result import Err, Ok, Result

from app.nutrition.api import errors
from app.nutrition.api.dto import MealtimeDTO, ResumedPupilIn
from app.nutrition.application import services
from app.nutrition.application.errors import NotFoundPupil, NotFoundSchoolClass
from app.nutrition.domain.pupil import CannotCancelAfterDeadline, CannotResumeAfterDeadline, PupilID
from app.nutrition.domain.request import CannotSubmitAfterDeadline
from app.nutrition.domain.time import Day, Period
from app.shared.api.errors import DomainValidationError
from app.shared.domain.school_class import ClassID


async def resume_pupil_on_day(
    pupil_id: str, day: date
) -> Result[None, errors.NotFoundPupilWithID | errors.CannotResumeAfterDeadline]:
    match await services.resume_pupil_on_day(pupil_id=PupilID(pupil_id), day=Day(day)):
        case Err(NotFoundPupil()):
            return Err(errors.NotFoundPupilWithID(pupil_id))

        case Err(CannotResumeAfterDeadline(deadline=deadline)):
            return Err(errors.CannotResumeAfterDeadline(deadline))

    return Ok(None)


async def cancel_pupil_for_period(
    pupil_id: str, start: date, end: date
) -> Result[None, DomainValidationError | errors.NotFoundPupilWithID | errors.CannotCancelAfterDeadline]:
    try:
        period = Period(start=start, end=end)
    except ValueError as error:
        return Err(DomainValidationError(message=str(error)))

    match await services.cancel_pupil_for_period(pupil_id=PupilID(pupil_id), period=period):
        case Err(NotFoundPupil()):
            return Err(errors.NotFoundPupilWithID(pupil_id))

        case Err(CannotCancelAfterDeadline(deadline=deadline)):
            return Err(errors.CannotCancelAfterDeadline(deadline))

    return Ok(None)


async def update_mealtimes_at_pupil(
    pupil_id: str, mealtimes: dict[MealtimeDTO, bool]
) -> Result[None, errors.NotFoundPupilWithID]:
    match await services.resume_or_cancel_mealtimes_at_pupil(
        pupil_id=PupilID(pupil_id), mealtimes={mealtime.to_model(): value for mealtime, value in mealtimes.items()}
    ):
        case Err(NotFoundPupil()):
            return Err(errors.NotFoundPupilWithID(pupil_id))

    return Ok(None)


async def submit_request_to_canteen(
    class_id: UUID, on_date: date, overrides: set[ResumedPupilIn]
) -> Result[None, errors.NotFoundSchoolClassWithID | errors.CannotSendRequestAfterDeadline]:
    match await services.submit_request_to_canteen(
        class_id=ClassID(class_id),
        on_date=on_date,
        overrides={PupilID(override.id): set(dto.to_model() for dto in override.mealtimes) for override in overrides},
    ):
        case Err(NotFoundSchoolClass()):
            return Err(errors.NotFoundSchoolClassWithID(class_id))

        case Err(CannotSubmitAfterDeadline(deadline=deadline)):
            return Err(errors.CannotSendRequestAfterDeadline(on_date, deadline))

    return Ok(None)
