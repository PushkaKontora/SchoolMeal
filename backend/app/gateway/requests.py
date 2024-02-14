from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, status
from result import Err

from app.nutrition.application import commands
from app.gateway.dto import SubmitRequestIn
from app.nutrition.application.errors import NotFoundSchoolClass
from app.nutrition.domain.pupil import PupilID
from app.nutrition.domain.request import CannotSentRequestAfterDeadline
from app.nutrition.domain.school_class import ClassID
from app.shared.exceptions import DomainException
from app.shared.fastapi import responses
from app.shared.fastapi.errors import BadRequestError, NotFoundError, UnprocessableEntityError
from app.shared.fastapi.schemas import OKSchema


router = APIRouter()


@router.post(
    "/school-classes/{class_id}/requests",
    summary="Отправить заявку на кухню",
    status_code=status.HTTP_201_CREATED,
    responses=responses.NOT_FOUND | responses.BAD_REQUEST,
)
async def submit_request_to_canteen(
    class_id: UUID, body: Annotated[SubmitRequestIn, Body()]
) -> OKSchema:
    try:
        class_id_ = ClassID(class_id)
        overrides = {PupilID(override.pupil_id): override.mealtimes for override in body.overrides}
    except DomainException as error:
        raise UnprocessableEntityError(error.message)

    submitting = await commands.submit_request_to_canteen(
        class_id=class_id_,
        on_date=body.on_date,
        overrides=overrides,
    )

    match submitting:
        case Err(NotFoundSchoolClass()):
            raise NotFoundError(f"Не найден класс с id={class_id}")

        case Err(CannotSentRequestAfterDeadline(deadline=deadline)):
            raise BadRequestError(f"Невозможно отправить заявку на {body.on_date} после {deadline.isoformat()}")

    return submitting.map(lambda _: OKSchema()).unwrap()
