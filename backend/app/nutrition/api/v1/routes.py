from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from result import Err

from app.nutrition.api.v1.schemas.bodies import (
    CancelPupilForPeriodBody,
    ResumePupilOnDayBody,
    SubmitRequestBody,
    UpdateMealtimesBody,
)
from app.nutrition.api.v1.schemas.params import (
    GetPortionsParams,
    GetPupilsParams,
    GetSchoolClassesParams,
    RequestIDParams,
)
from app.nutrition.api.v1.schemas.view import PortionsReportOut, PupilOut, RequestOut, SchoolClassOut
from app.nutrition.application import services
from app.nutrition.application.dao.pupils import IPupilRepository, PupilByClassID
from app.nutrition.application.dao.requests import IRequestRepository, RequestByDate, RequestByStatus
from app.nutrition.application.dao.school_classes import ClassByNumberRange, ISchoolClassRepository
from app.nutrition.application.errors import NotFoundPupil, NotFoundSchoolClass
from app.nutrition.domain.pupil import CannotCancelAfterDeadline, CannotResumeAfterDeadline, PupilID
from app.nutrition.domain.request import CannotSubmitAfterDeadline, RequestStatus
from app.nutrition.domain.school_class import ClassID
from app.nutrition.domain.time import Day, Period
from app.nutrition.infrastructure.dependencies import NutritionContainer
from app.shared.api import responses
from app.shared.api.errors import BadRequest, NotFound, UnprocessableEntity
from app.shared.api.schemas import OKSchema


router = APIRouter()


@router.get(
    "/school-classes",
    summary="Получить список классов",
    status_code=status.HTTP_200_OK,
)
@inject
async def get_school_classes(
    params: Annotated[GetSchoolClassesParams, Depends()],
    class_repository: ISchoolClassRepository = Depends(Provide[NutritionContainer.class_repository]),
) -> list[SchoolClassOut]:
    classes = await class_repository.all(spec=params.to_specification())

    return [SchoolClassOut.from_model(school_class) for school_class in classes]


@router.get(
    "/pupils",
    summary="Получить список учеников",
    status_code=status.HTTP_200_OK,
)
@inject
async def get_pupils(
    params: Annotated[GetPupilsParams, Depends()],
    pupil_repository: IPupilRepository = Depends(Provide[NutritionContainer.pupil_repository]),
) -> list[PupilOut]:
    pupils = await pupil_repository.all(spec=params.to_specification())

    return [PupilOut.from_model(pupil) for pupil in pupils]


@router.get(
    "/pupils/{pupil_id}",
    summary="Получить информацию об ученике",
    status_code=status.HTTP_200_OK,
    responses=responses.UNPROCESSABLE_ENTITY | responses.NOT_FOUND,
)
@inject
async def get_pupil(
    pupil_id: str,
    pupil_repository: IPupilRepository = Depends(Provide[NutritionContainer.pupil_repository]),
) -> PupilOut:
    try:
        pupil_id_ = PupilID(pupil_id)
    except ValueError as error:
        raise UnprocessableEntity(str(error)) from error

    pupil = await pupil_repository.get(ident=pupil_id_)

    if not pupil:
        raise NotFound(f"Не существует ученика с id={pupil_id}")

    return PupilOut.from_model(pupil)


@router.get(
    "/requests",
    summary="Получить отправленную заявку",
    status_code=status.HTTP_200_OK,
    responses=responses.UNPROCESSABLE_ENTITY | responses.NOT_FOUND,
)
@inject
async def get_submitted_request(
    params: Annotated[RequestIDParams, Depends()],
    request_repository: IRequestRepository = Depends(Provide[NutritionContainer.request_repository]),
    pupil_repository: IPupilRepository = Depends(Provide[NutritionContainer.pupil_repository]),
) -> RequestOut:
    try:
        class_id = ClassID(params.class_id)
    except ValueError as error:
        raise UnprocessableEntity(str(error))

    request = await request_repository.get(class_id=class_id, on_date=params.on_date)

    if not request:
        raise NotFound(f"Заявка для класса {params.class_id} на {params.on_date.isoformat()} ещё не отправлена")

    pupils = await pupil_repository.all(PupilByClassID(class_id))

    return RequestOut.from_models(request, pupils)


@router.get(
    "/requests/prefill",
    summary="Предзаполнить заявку",
    status_code=status.HTTP_200_OK,
    responses=responses.UNPROCESSABLE_ENTITY | responses.BAD_REQUEST,
)
@inject
async def prefill_request(
    params: Annotated[RequestIDParams, Depends()],
    class_repository: ISchoolClassRepository = Depends(Provide[NutritionContainer.class_repository]),
    pupil_repository: IPupilRepository = Depends(Provide[NutritionContainer.pupil_repository]),
) -> RequestOut:
    try:
        class_id = ClassID(params.class_id)
    except ValueError as error:
        raise UnprocessableEntity(str(error)) from error

    result = await services.prefill_request(
        class_id=class_id,
        on_date=params.on_date,
        overrides={},
        class_repository=class_repository,
        pupil_repository=pupil_repository,
    )

    match result:
        case Err(NotFoundSchoolClass()):
            raise BadRequest(f"Не существует класса с id={params.class_id}")

    request = result.unwrap()
    pupils = await pupil_repository.all(PupilByClassID(class_id))

    return RequestOut.from_models(request, pupils)


@router.get(
    "/portions",
    summary="Получить количество порций",
    status_code=status.HTTP_200_OK,
)
@inject
async def get_portions(
    params: Annotated[GetPortionsParams, Depends()],
    request_repository: IRequestRepository = Depends(Provide[NutritionContainer.request_repository]),
    class_repository: ISchoolClassRepository = Depends(Provide[NutritionContainer.class_repository]),
) -> PortionsReportOut:
    requests = await request_repository.all(RequestByDate(params.on_date) & RequestByStatus(RequestStatus.SUBMITTED))

    start, end = params.class_type.to_model_range()
    classes = await class_repository.all(ClassByNumberRange(start=start, end=end))

    return PortionsReportOut.create(classes, requests)


@router.post(
    "/requests",
    summary="Отправить заявку на кухню",
    status_code=status.HTTP_201_CREATED,
    responses=responses.UNPROCESSABLE_ENTITY | responses.BAD_REQUEST,
)
@inject
async def submit_request_to_canteen(
    body: SubmitRequestBody,
    request_repository: IRequestRepository = Depends(Provide[NutritionContainer.request_repository]),
    class_repository: ISchoolClassRepository = Depends(Provide[NutritionContainer.class_repository]),
    pupil_repository: IPupilRepository = Depends(Provide[NutritionContainer.pupil_repository]),
) -> OKSchema:
    try:
        class_id = ClassID(body.class_id)
        overrides = {
            PupilID(pupil.id): {mealtime.to_model() for mealtime in pupil.mealtimes} for pupil in body.overrides
        }
    except ValueError as error:
        raise UnprocessableEntity(str(error)) from error

    result = await services.submit_request_to_canteen(
        class_id=class_id,
        on_date=body.on_date,
        overrides=overrides,
        class_repository=class_repository,
        pupil_repository=pupil_repository,
        request_repository=request_repository,
    )

    match result:
        case Err(NotFoundSchoolClass()):
            raise BadRequest(f"Не существует класса с id={body.class_id}")

        case Err(CannotSubmitAfterDeadline(deadline=deadline)):
            raise BadRequest(f"Невозможно отправить заявку на {deadline.date()} после {deadline.timetz().isoformat()}")

    return OKSchema()


@router.post(
    "/pupils/{pupil_id}/resume",
    summary="Поставить ученика на питание на день",
    status_code=status.HTTP_200_OK,
    responses=responses.UNPROCESSABLE_ENTITY | responses.NOT_FOUND | responses.BAD_REQUEST,
)
@inject
async def resume_pupil_on_day(
    pupil_id: str,
    body: ResumePupilOnDayBody,
    pupil_repository: IPupilRepository = Depends(Provide[NutritionContainer.pupil_repository]),
) -> OKSchema:
    try:
        pupil_id_ = PupilID(pupil_id)
        day = Day(body.day)
    except ValueError as error:
        raise UnprocessableEntity(str(error)) from error

    result = await services.resume_pupil_on_day(pupil_id=pupil_id_, day=day, pupil_repository=pupil_repository)

    match result:
        case Err(NotFoundPupil()):
            raise NotFound(f"Не существует ученика с id={pupil_id}")

        case Err(CannotResumeAfterDeadline(deadline=deadline)):
            raise BadRequest(
                f"Невозможно поставить ребёнка на питание в день {deadline.date()} после {deadline.timetz().isoformat()}"
            )

    return OKSchema()


@router.post(
    "/pupils/{pupil_id}/cancel",
    summary="Снять ученика с питания на период",
    status_code=status.HTTP_200_OK,
    responses=responses.UNPROCESSABLE_ENTITY | responses.NOT_FOUND | responses.BAD_REQUEST,
)
@inject
async def cancel_pupil_for_period(
    pupil_id: str,
    body: CancelPupilForPeriodBody,
    pupil_repository: IPupilRepository = Depends(Provide[NutritionContainer.pupil_repository]),
) -> OKSchema:
    try:
        pupil_id_ = PupilID(pupil_id)
        period = Period(start=body.start, end=body.end)
    except ValueError as error:
        raise UnprocessableEntity(str(error)) from error

    result = await services.cancel_pupil_for_period(
        pupil_id=pupil_id_, period=period, pupil_repository=pupil_repository
    )

    match result:
        case Err(NotFoundPupil()):
            raise NotFound(f"Не существует ученика с id={pupil_id}")

        case Err(CannotCancelAfterDeadline(deadline=deadline)):
            raise BadRequest(
                f"Невозможно снять ребёнка с питания на {deadline.date()} после {deadline.timetz().isoformat()}"
            )

    return OKSchema()


@router.patch(
    "/pupils/{pupil_id}/mealtimes",
    summary="Поставить или снять приёмы пищи у ученика",
    status_code=status.HTTP_200_OK,
    responses=responses.UNPROCESSABLE_ENTITY | responses.NOT_FOUND,
)
@inject
async def update_mealtimes_at_pupil(
    pupil_id: str,
    body: UpdateMealtimesBody,
    pupil_repository: IPupilRepository = Depends(Provide[NutritionContainer.pupil_repository]),
) -> OKSchema:
    try:
        pupil_id_ = PupilID(pupil_id)
        mealtimes = {mealtime.to_model(): resumed for mealtime, resumed in body.mealtimes.items()}
    except ValueError as error:
        raise UnprocessableEntity(str(error)) from error

    result = await services.resume_or_cancel_mealtimes_at_pupil(
        pupil_id=pupil_id_,
        mealtimes=mealtimes,
        pupil_repository=pupil_repository,
    )

    match result:
        case Err(NotFoundPupil()):
            raise NotFound(f"Не существует ученика с id={pupil_id}")

    return OKSchema()
