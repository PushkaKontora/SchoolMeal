from fastapi import APIRouter, status
from result import Err

from app.gateway import responses
from app.gateway.errors import BadRequest, NotFound, UnprocessableEntity
from app.gateway.mobile.v1.pupils.dto import CancelPupilForPeriodBody, ResumePupilOnDayBody, UpdateMealtimesBody
from app.gateway.mobile.v1.pupils.view import ChildSummaryOut
from app.nutrition.api import dto as nutrition_dto, errors as nutrition_errors, handlers as nutrition_api
from app.shared.api.errors import DomainValidationError
from app.shared.fastapi.dependencies.headers import AuthorizedUserDep
from app.shared.fastapi.schemas import OKSchema
from app.structure.api import dto as structure_dto, errors as structure_errors, handlers as structure_api


router = APIRouter(prefix="/pupils")


@router.get(
    "",
    summary="Получить список детей пользователя",
    status_code=status.HTTP_200_OK,
)
async def get_children(user: AuthorizedUserDep) -> list[ChildSummaryOut]:
    pupils = await structure_api.get_pupils(filters=structure_dto.PupilFilters(parent_id=user.id))
    school = await structure_api.get_school_info()
    classes = await structure_api.get_classes(
        filters=structure_dto.ClassesFilters(ids={pupil.class_id for pupil in pupils})
    )
    meals = await nutrition_api.get_pupils(filters=nutrition_dto.PupilFilters(ids={pupil.id for pupil in pupils}))

    return ChildSummaryOut.create_many(pupils, meals, school, classes)


@router.get(
    "/{pupil_id}",
    summary="Получить информацию о питании ребёнка",
    status_code=status.HTTP_200_OK,
)
async def get_child(pupil_id: str) -> nutrition_api.PupilOut:
    pupil = await nutrition_api.get_pupil(pupil_id)

    if not pupil:
        raise NotFound(f"Не найден ученик с id={pupil_id}")

    return pupil


@router.post(
    "/{pupil_id}/resume",
    summary="Поставить ученика на питание на день",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def resume_pupil_on_day(pupil_id: str, body: ResumePupilOnDayBody) -> OKSchema:
    match await nutrition_api.resume_pupil_on_day(pupil_id=pupil_id, day=body.day):
        case Err(nutrition_errors.NotFoundPupilWithID(message=message)):
            raise NotFound(message)

        case Err(nutrition_errors.CannotResumeAfterDeadline(message=message)):
            raise BadRequest(message)

    return OKSchema()


@router.post(
    "/{pupil_id}/cancel",
    summary="Снять ученика с питания на период",
    status_code=status.HTTP_200_OK,
    responses=responses.UNPROCESSABLE_ENTITY | responses.NOT_FOUND,
)
async def cancel_pupil_for_period(pupil_id: str, body: CancelPupilForPeriodBody) -> OKSchema:
    match await nutrition_api.cancel_pupil_for_period(pupil_id=pupil_id, start=body.start, end=body.end):
        case Err(DomainValidationError(message=message)):
            raise UnprocessableEntity(message)

        case Err(nutrition_errors.NotFoundPupilWithID(message=message)):
            raise NotFound(message)

        case Err(nutrition_errors.CannotCancelAfterDeadline(message=message)):
            raise BadRequest(message)

    return OKSchema()


@router.patch(
    "/{pupil_id}/mealtimes",
    summary="Поставить или снять приёмы пищи у ученика",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def update_mealtimes_at_pupil(pupil_id: str, body: UpdateMealtimesBody) -> OKSchema:
    match await nutrition_api.update_mealtimes_at_pupil(pupil_id=pupil_id, mealtimes=body.mealtimes):
        case Err(nutrition_errors.NotFoundPupilWithID(message=message)):
            raise NotFound(message)

    return OKSchema()


@router.post(
    "/{pupil_id}/attach",
    summary="Закрепить ребёнка за родителем",
    status_code=status.HTTP_200_OK,
    responses=responses.BAD_REQUEST,
)
async def attach_pupil_to_parent(pupil_id: str, user: AuthorizedUserDep) -> OKSchema:
    match await structure_api.attach_pupil_to_parent(parent_id=user.id, pupil_id=pupil_id):
        case Err(structure_errors.NotFoundParentWithID(message=message)):
            raise NotFound(message)

        case Err(structure_errors.NotFoundPupilWithID(message=message)):
            raise NotFound(message)

        case Err(structure_errors.PupilIsAlreadyAttached(message=message)):
            raise BadRequest(message)

    return OKSchema()
