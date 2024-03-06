from dependency_injector.wiring import Provide, inject
from result import Err, Ok, Result

from app.nutrition.api import errors
from app.nutrition.api.dto import (
    AttachPupilToParentIn,
    CancelPupilForPeriodIn,
    ResumePupilOnDayIn,
    SubmitRequestToCanteenIn,
    UpdateMealtimesAtPupilIn,
)
from app.nutrition.api.errors import NotFoundSchoolClassWithID
from app.nutrition.application import services
from app.nutrition.application.dao import (
    IParentRepository,
    IPupilRepository,
    IRequestRepository,
    ISchoolClassRepository,
)
from app.nutrition.application.errors import NotFoundParent, NotFoundPupil, NotFoundSchoolClass
from app.nutrition.domain.parent import ParentID, PupilIsAlreadyAttached
from app.nutrition.domain.pupil import PupilID
from app.nutrition.domain.request import CannotSubmitAfterDeadline
from app.nutrition.domain.school_class import ClassID
from app.nutrition.domain.times import Day, Period
from app.nutrition.infrastructure.dependencies import NutritionContainer
from app.shared.api.errors import ValidationError


@inject
async def resume_pupil_on_day(
    command: ResumePupilOnDayIn, pupil_repository: IPupilRepository = Provide[NutritionContainer.pupil_repository]
) -> Result[None, errors.NotFoundPupilWithID]:
    pupil_id, day = PupilID(command.pupil_id), Day(command.day)

    match await services.resume_pupil_on_day(pupil_id, day, pupil_repository):
        case Err(NotFoundPupil()):
            return Err(errors.NotFoundPupilWithID(pupil_id.value))

    return Ok(None)


@inject
async def cancel_pupil_for_period(
    command: CancelPupilForPeriodIn,
    pupil_repository: IPupilRepository = Provide[NutritionContainer.pupil_repository],
) -> Result[None, ValidationError | errors.NotFoundPupilWithID]:
    try:
        pupil_id = PupilID(command.pupil_id)
        period = Period(start=command.start, end=command.end)
    except ValueError as error:
        return Err(ValidationError(str(error)))

    match await services.cancel_pupil_for_period(pupil_id, period, pupil_repository):
        case Err(NotFoundPupil()):
            return Err(errors.NotFoundPupilWithID(pupil_id.value))

    return Ok(None)


@inject
async def update_mealtimes_at_pupil(
    command: UpdateMealtimesAtPupilIn,
    pupil_repository: IPupilRepository = Provide[NutritionContainer.pupil_repository],
) -> Result[None, errors.NotFoundPupilWithID]:
    pupil_id = PupilID(command.pupil_id)
    mealtimes = {mealtime.to_model(): value for mealtime, value in command.mealtimes.items()}

    match await services.resume_or_cancel_mealtimes_at_pupil(pupil_id, mealtimes, pupil_repository):
        case Err(NotFoundPupil()):
            return Err(errors.NotFoundPupilWithID(pupil_id.value))

    return Ok(None)


@inject
async def submit_request_to_canteen(
    command: SubmitRequestToCanteenIn,
    class_repository: ISchoolClassRepository = Provide[NutritionContainer.class_repository],
    pupil_repository: IPupilRepository = Provide[NutritionContainer.pupil_repository],
    request_repository: IRequestRepository = Provide[NutritionContainer.request_repository],
) -> Result[None, errors.NotFoundSchoolClassWithID | errors.CannotSentRequestAfterDeadline]:
    class_id = ClassID(command.class_id)
    overrides = {
        PupilID(override.id): set(dto.to_model() for dto in override.mealtimes) for override in command.overrides
    }
    day = Day(command.on_date)

    match await services.submit_request_to_canteen(
        class_id, day, overrides, class_repository, pupil_repository, request_repository
    ):
        case Err(NotFoundSchoolClass()):
            return Err(NotFoundSchoolClassWithID(class_id.value))

        case Err(CannotSubmitAfterDeadline(deadline=deadline)):
            return Err(errors.CannotSentRequestAfterDeadline(day.value, deadline))

    return Ok(None)


@inject
async def attach_pupil_to_parent(
    command: AttachPupilToParentIn,
    parent_repository: IParentRepository = Provide[NutritionContainer.parent_repository],
    pupil_repository: IPupilRepository = Provide[NutritionContainer.pupil_repository],
) -> Result[None, errors.NotFoundParentWithID | errors.NotFoundPupilWithID | errors.PupilIsAlreadyAttached]:
    parent_id, pupil_id = ParentID(command.parent_id), PupilID(command.pupil_id)

    match await services.attach_child_to_parent(parent_id, pupil_id, parent_repository, pupil_repository):
        case Err(NotFoundParent()):
            return Err(errors.NotFoundParentWithID(parent_id.value))

        case Err(NotFoundPupil()):
            return Err(errors.NotFoundPupilWithID(pupil_id.value))

        case Err(PupilIsAlreadyAttached()):
            return Err(errors.PupilIsAlreadyAttached())

    return Ok(None)
