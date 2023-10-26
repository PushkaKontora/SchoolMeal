from fastapi import APIRouter

from app.account.api.dependencies import UsersRepositoryDep
from app.account.api.registration.schemas import IncorrectRegistrationFormError, ParentRegistrationForm
from app.account.application.use_cases.registration import AlreadyRegisteredPhoneError, register_parent
from app.common.api.dependencies import SessionDep
from app.common.api.errors import LogicError, ValidationModelError
from app.common.api.schemas import HTTPError, OKSchema


router = APIRouter()


@router.post(
    "/register-parent",
    summary="Регистрация родителя",
    status_code=201,
    responses={400: {"model": HTTPError}, 422: {"model": HTTPError}},
)
async def register_parent_(
    session: SessionDep, form: ParentRegistrationForm, users_repository: UsersRepositoryDep
) -> OKSchema:
    try:
        first_name, last_name, phone, email, password = form.to_model()

        async with session.begin():
            await register_parent(first_name, last_name, phone, email, password, users_repository)

    except IncorrectRegistrationFormError as error:
        raise ValidationModelError(detail=str(error)) from error

    except AlreadyRegisteredPhoneError as error:
        raise LogicError(detail=str(error)) from error

    return OKSchema()
