from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from result import Err

from app.gateway import responses
from app.gateway.errors import BadRequest, NotFound
from app.gateway.web.requests.dto import GetOrPrefillRequestParams, SubmitRequestBody
from app.gateway.web.requests.view import PrefilledRequestOut
from app.nutrition.api import dto as nutrition_dto, errors as nutrition_errors, handlers as nutrition_api
from app.shared.fastapi.schemas import OKSchema
from app.structure.api import dto as structure_dto, handlers as structure_api


router = APIRouter()


@router.get(
    "/school-classes/{class_id}/requests/prefill",
    summary="Получить или предзаполнить заявку",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def get_or_prefill_request(
    class_id: UUID, params: Annotated[GetOrPrefillRequestParams, Depends()]
) -> PrefilledRequestOut:
    prefilling = await nutrition_api.get_or_prefill_request(class_id=class_id, on_date=params.on_date)

    match prefilling:
        case Err(nutrition_errors.NotFoundSchoolClassWithID(message=message)):
            raise NotFound(message)

    request = prefilling.unwrap()
    pupils = await structure_api.get_pupils(
        filters=structure_dto.PupilFilters(ids=set(declaration.pupil_id for declaration in request.declarations))
    )
    nutrition_pupils = await nutrition_api.get_pupils(
        filters=nutrition_dto.PupilFilters(ids={pupil.id for pupil in pupils})
    )

    return PrefilledRequestOut.create(request, pupils, nutrition_pupils)


@router.post(
    "/school-classes/{class_id}/requests",
    summary="Отправить заявку на кухню",
    status_code=status.HTTP_201_CREATED,
    responses=responses.NOT_FOUND | responses.BAD_REQUEST,
)
async def submit_request_to_canteen(class_id: UUID, body: SubmitRequestBody) -> OKSchema:
    match await nutrition_api.submit_request_to_canteen(
        class_id=class_id, on_date=body.on_date, overrides=body.overrides
    ):
        case Err(nutrition_errors.NotFoundSchoolClassWithID(message=message)):
            raise NotFound(message)

        case Err(nutrition_errors.CannotSendRequestAfterDeadline(message=message)):
            raise BadRequest(message)

    return OKSchema()
