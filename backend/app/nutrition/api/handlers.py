from datetime import date
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from result import Err, Ok, Result

from app.nutrition.api import errors
from app.nutrition.api.dto import MealtimeDTO, PupilFilters, PupilOut, RequestOut, ResumedPupilIn
from app.nutrition.application import services
from app.nutrition.application.dao.pupils import IPupilRepository
from app.nutrition.application.dao.requests import IRequestRepository, RequestByDate, RequestByStatus
from app.nutrition.application.dao.school_classes import ISchoolClassRepository
from app.nutrition.application.errors import NotFoundPupil, NotFoundSchoolClass
from app.nutrition.domain.pupil import CannotCancelAfterDeadline, CannotResumeAfterDeadline, PupilID
from app.nutrition.domain.request import CannotSubmitAfterDeadline, RequestStatus
from app.nutrition.domain.time import Day, Period
from app.nutrition.infrastructure.dependencies import NutritionContainer
from app.shared.api.errors import DomainValidationError
from app.shared.domain.school_class import ClassID


@inject
async def get_pupils(
    filters: PupilFilters, pupil_repository: IPupilRepository = Provide[NutritionContainer.pupil_repository]
) -> list[PupilOut]:
    pupils = await pupil_repository.all(spec=filters.to_specification())

    return [PupilOut.from_model(pupil) for pupil in pupils]


@inject
async def get_pupil(
    pupil_id: str, pupil_repository: IPupilRepository = Provide[NutritionContainer.pupil_repository]
) -> PupilOut | None:
    pupil = await pupil_repository.get(ident=PupilID(pupil_id))

    return PupilOut.from_model(pupil) if pupil else None


@inject
async def get_or_prefill_request(
    class_id: UUID,
    on_date: date,
    class_repository: ISchoolClassRepository = Provide[NutritionContainer.class_repository],
    pupil_repository: IPupilRepository = Provide[NutritionContainer.pupil_repository],
    request_repository: IRequestRepository = Provide[NutritionContainer.request_repository],
) -> Result[RequestOut, errors.NotFoundSchoolClassWithID]:
    class_id_ = ClassID(class_id)

    request = await request_repository.get(class_id_, on_date)

    if not request:
        prefilling = await services.prefill_request(
            class_id_, on_date, overrides={}, class_repository=class_repository, pupil_repository=pupil_repository
        )

        match prefilling:
            case Err(NotFoundSchoolClass()):
                return Err(errors.NotFoundSchoolClassWithID(class_id))

        request = prefilling.unwrap()

    return Ok(RequestOut.from_model(request))


@inject
async def get_submitted_requests_on_date(
    on_date: date,
    request_repository: IRequestRepository = Provide[NutritionContainer.request_repository],
) -> list[RequestOut]:
    requests = await request_repository.all(spec=RequestByDate(on_date) & RequestByStatus(RequestStatus.SUBMITTED))

    return [RequestOut.from_model(request) for request in requests]


@inject
async def resume_pupil_on_day(
    pupil_id: str, day: date, pupil_repository: IPupilRepository = Provide[NutritionContainer.pupil_repository]
) -> Result[None, errors.NotFoundPupilWithID | errors.CannotResumeAfterDeadline]:
    match await services.resume_pupil_on_day(
        pupil_id=PupilID(pupil_id), day=Day(day), pupil_repository=pupil_repository
    ):
        case Err(NotFoundPupil()):
            return Err(errors.NotFoundPupilWithID(pupil_id))

        case Err(CannotResumeAfterDeadline(deadline=deadline)):
            return Err(errors.CannotResumeAfterDeadline(deadline))

    return Ok(None)


@inject
async def cancel_pupil_for_period(
    pupil_id: str,
    start: date,
    end: date,
    pupil_repository: IPupilRepository = Provide[NutritionContainer.pupil_repository],
) -> Result[None, DomainValidationError | errors.NotFoundPupilWithID | errors.CannotCancelAfterDeadline]:
    try:
        period = Period(start=start, end=end)
    except ValueError as error:
        return Err(DomainValidationError(message=str(error)))

    match await services.cancel_pupil_for_period(
        pupil_id=PupilID(pupil_id), period=period, pupil_repository=pupil_repository
    ):
        case Err(NotFoundPupil()):
            return Err(errors.NotFoundPupilWithID(pupil_id))

        case Err(CannotCancelAfterDeadline(deadline=deadline)):
            return Err(errors.CannotCancelAfterDeadline(deadline))

    return Ok(None)


@inject
async def update_mealtimes_at_pupil(
    pupil_id: str,
    mealtimes: dict[MealtimeDTO, bool],
    pupil_repository: IPupilRepository = Provide[NutritionContainer.pupil_repository],
) -> Result[None, errors.NotFoundPupilWithID]:
    match await services.resume_or_cancel_mealtimes_at_pupil(
        pupil_id=PupilID(pupil_id),
        mealtimes={mealtime.to_model(): value for mealtime, value in mealtimes.items()},
        pupil_repository=pupil_repository,
    ):
        case Err(NotFoundPupil()):
            return Err(errors.NotFoundPupilWithID(pupil_id))

    return Ok(None)


@inject
async def submit_request_to_canteen(
    class_id: UUID,
    on_date: date,
    overrides: set[ResumedPupilIn],
    class_repository: ISchoolClassRepository = Provide[NutritionContainer.class_repository],
    pupil_repository: IPupilRepository = Provide[NutritionContainer.pupil_repository],
    request_repository: IRequestRepository = Provide[NutritionContainer.request_repository],
) -> Result[None, errors.NotFoundSchoolClassWithID | errors.CannotSendRequestAfterDeadline]:
    match await services.submit_request_to_canteen(
        class_id=ClassID(class_id),
        on_date=on_date,
        overrides={PupilID(override.id): set(dto.to_model() for dto in override.mealtimes) for override in overrides},
        class_repository=class_repository,
        pupil_repository=pupil_repository,
        request_repository=request_repository,
    ):
        case Err(NotFoundSchoolClass()):
            return Err(errors.NotFoundSchoolClassWithID(class_id))

        case Err(CannotSubmitAfterDeadline(deadline=deadline)):
            return Err(errors.CannotSendRequestAfterDeadline(on_date, deadline))

    return Ok(None)
