from uuid import UUID

from fastapi import APIRouter, status
from result import Err

from app.gateway import responses
from app.gateway.errors import BadRequest, NotFound
from app.gateway.web.requests.dto import SubmitRequestBody
from app.nutrition.api import handlers as nutrition_api
from app.nutrition.api.errors import CannotSentRequestAfterDeadline, NotFoundSchoolClassWithID
from app.shared.fastapi.schemas import OKSchema


router = APIRouter()


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
        case Err(NotFoundSchoolClassWithID(message=message)):
            raise NotFound(message)

        case Err(CannotSentRequestAfterDeadline(message=message)):
            raise BadRequest(message)

    return OKSchema()
