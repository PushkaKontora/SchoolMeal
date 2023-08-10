from fastapi import APIRouter, Body, Depends
from starlette import status

from app.common.gateway.dto import OKModel
from app.common.gateway.responses import response_400, response_422
from app.user.application.services import UserService
from app.user.domain.errors import (
    EmptyFirstNameError,
    EmptyLastNameError,
    EmptyPasswordError,
    InvalidEmailFormatError,
    InvalidPhoneFormatError,
    NotUniqueUserDataError,
)
from app.user.gateway.rest.dependencies import get_user_service
from app.user.gateway.rest.users.dto import RegistrationParentForm
from app.user.gateway.rest.users.errors import (
    EmailValidationError,
    FirstNameValidationError,
    LastNameValidationError,
    NotUniqueLoginOrPhoneOrEmailError,
    PasswordValidationError,
    PhoneValidationError,
)


router = APIRouter()


@router.post(
    path="/register-parent",
    summary="Зарегистрировать родителя",
    status_code=status.HTTP_201_CREATED,
    response_model=OKModel,
    responses=response_400 | response_422,  # type: ignore
)
async def register_parent(
    form: RegistrationParentForm = Body(), user_service: UserService = Depends(get_user_service)
) -> OKModel:
    try:
        await user_service.register_parent(
            phone=form.phone,
            password=form.password,
            first_name=form.first_name,
            last_name=form.last_name,
            email=form.email,
        )

    except InvalidPhoneFormatError as error:
        raise PhoneValidationError from error

    except EmptyPasswordError as error:
        raise PasswordValidationError from error

    except EmptyFirstNameError as error:
        raise FirstNameValidationError from error

    except EmptyLastNameError as error:
        raise LastNameValidationError from error

    except InvalidEmailFormatError as error:
        raise EmailValidationError from error

    except NotUniqueUserDataError as error:
        raise NotUniqueLoginOrPhoneOrEmailError from error

    return OKModel()
