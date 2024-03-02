from uuid import UUID

from fastapi import APIRouter, status
from result import Ok, do

from app.gateway.dependencies import NutritionAPIDep
from app.gateway.web.dto import SubmitRequestIn
from app.shared.fastapi import responses
from app.shared.fastapi.errors import BadRequest
from app.shared.fastapi.schemas import OKSchema


router = APIRouter()


@router.post(
    "/school-classes/{class_id}/requests",
    summary="Отправить заявку на кухню",
    status_code=status.HTTP_201_CREATED,
    responses=responses.NOT_FOUND | responses.BAD_REQUEST,
)
async def submit_request_to_canteen(class_id: UUID, body: SubmitRequestIn, nutrition_api: NutritionAPIDep) -> OKSchema:
    return do(
        Ok(OKSchema())
        for _ in await nutrition_api.submit_request_to_canteen(
            class_id=class_id,
            on_date=body.on_date,
            overrides=body.overrides,
        )
    ).unwrap_or_raise(BadRequest)
