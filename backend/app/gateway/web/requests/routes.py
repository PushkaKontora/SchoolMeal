from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from result import Err

from app.gateway import responses
from app.gateway.errors import BadRequest, NotFound
from app.gateway.web.requests.dto import (
    GetOrPrefillRequestParams,
    GetPortionReportBySubmittedRequestsParams,
    SubmitRequestBody,
)
from app.gateway.web.requests.view import PortionsReportOut, PrefilledRequestOut
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


@router.get(
    "/portions",
    summary="Получить количество порций по отправленным заявкам",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND,
)
async def get_portion_report_by_submitted_requests(
    params: Annotated[GetPortionReportBySubmittedRequestsParams, Depends()]
) -> PortionsReportOut:
    school_classes = await structure_api.get_classes(filters=structure_dto.ClassesFilters(class_type=params.class_type))
    requests = await nutrition_api.get_submitted_requests_on_date(on_date=params.on_date)

    return PortionsReportOut.create(school_classes, requests)


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
