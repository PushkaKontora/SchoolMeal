from uuid import UUID

from fastapi import APIRouter, status
from result import Err, as_result

from app.gateway.web.dto import SubmitRequestIn
from app.nutrition.application import commands
from app.nutrition.application.errors import NotFoundSchoolClass
from app.nutrition.domain.pupil import PupilID
from app.nutrition.domain.request import CannotSentRequestAfterDeadline
from app.nutrition.domain.school_class import ClassID
from app.shared.fastapi import responses
from app.shared.fastapi.errors import BadRequest, NotFound, UnprocessableEntity
from app.shared.fastapi.schemas import OKSchema


router = APIRouter()


@router.post(
    "/school-classes/{class_id}/requests",
    summary="Отправить заявку на кухню",
    status_code=status.HTTP_201_CREATED,
    responses=responses.NOT_FOUND | responses.BAD_REQUEST,
)
async def submit_request_to_canteen(class_id: UUID, body: SubmitRequestIn) -> OKSchema:
    id_ = as_result(ValueError)(lambda x: ClassID(x))(class_id).unwrap_or_raise(UnprocessableEntity)
    overrides = as_result(ValueError)(lambda x: {PupilID(override.pupil_id): override.mealtimes for override in x})(
        body.overrides
    ).unwrap_or_raise(UnprocessableEntity)

    submitting = await commands.submit_request_to_canteen(class_id=id_, on_date=body.on_date, overrides=overrides)

    match submitting:
        case Err(NotFoundSchoolClass()):
            raise NotFound(f"Не найден класс с id={class_id}")

        case Err(CannotSentRequestAfterDeadline(deadline=deadline)):
            raise BadRequest(f"Невозможно отправить заявку на {body.on_date} после {deadline.isoformat()}")

    return submitting.map(lambda _: OKSchema()).unwrap()
