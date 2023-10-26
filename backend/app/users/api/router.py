from fastapi import APIRouter, Response, status

from app.common.api import responses
from app.common.api.dependencies import SessionDep
from app.common.api.errors import BadRequestError, NotFoundError, UnprocessableEntityError
from app.common.api.schemas import OKSchema
from app.users.api.dependencies.services import SessionServiceDep, UserServiceDep
from app.users.api.dependencies.settings import JWTSettingsDep
from app.users.api.dependencies.tokens import (
    AccessTokenDep,
    RefreshTokenDep,
    delete_refresh_from_cookies,
    set_refresh_in_cookies,
)
from app.users.api.schemas import AccessTokenOut, CredentialIn, ParentRegistrationForm, UserOut
from app.users.application.repositories import NotFoundUser
from app.users.application.services import IncorrectLoginOrPassword, PhoneBelongsToAnotherParent
from app.users.domain import passwords, phone
from app.users.domain.email import InvalidEmailFormat
from app.users.domain.names import FirstNameContainsNotCyrillicCharacters, LastNameContainsNotCyrillicCharacters
from app.users.domain.session import CantRevokeAlreadyRevokedSession
from app.users.domain.tokens import SignatureIsBroken, TokenHasExpired


router = APIRouter()


@router.post(
    "/authenticate",
    summary="Аутентификация по логину и паролю",
    status_code=status.HTTP_200_OK,
    responses=responses.BAD_REQUEST | responses.UNPROCESSABLE_ENTITY,
)
async def authenticate(
    response: Response,
    credential: CredentialIn,
    session: SessionDep,
    user_service: UserServiceDep,
    jwt_settings: JWTSettingsDep,
) -> AccessTokenOut:
    try:
        async with session.begin():
            access_token, refresh_token = await user_service.authenticate(
                login=credential.login,
                password=credential.password,
            )
            await session.commit()

    except IncorrectLoginOrPassword as error:
        raise BadRequestError("Неверный логин или пароль") from error

    set_refresh_in_cookies(response, refresh_token, secret=jwt_settings.secret.get_secret_value())

    return AccessTokenOut.from_model(access_token, secret=jwt_settings.secret.get_secret_value())


@router.post(
    "/logout", summary="Выход из аккаунта", status_code=status.HTTP_200_OK, responses=responses.UNPROCESSABLE_ENTITY
)
async def logout(
    response: Response,
    session: SessionDep,
    access_token: AccessTokenDep,
    user_service: UserServiceDep,
) -> OKSchema:
    try:
        async with session.begin():
            await user_service.logout(access_token)
            await session.commit()

    except SignatureIsBroken as error:
        raise UnprocessableEntityError("Сигнатура токена повреждена") from error

    except TokenHasExpired as error:
        raise UnprocessableEntityError("Время жизни токена истекло") from error

    delete_refresh_from_cookies(response)

    return OKSchema()


@router.post(
    "/refresh-tokens",
    summary="Перевыпустить токены",
    status_code=status.HTTP_200_OK,
    responses=responses.BAD_REQUEST | responses.UNPROCESSABLE_ENTITY,
)
async def refresh_tokens(
    response: Response,
    session: SessionDep,
    refresh_token: RefreshTokenDep,
    session_service: SessionServiceDep,
    jwt_settings: JWTSettingsDep,
) -> AccessTokenOut:
    try:
        async with session.begin():
            try:
                access, refresh = await session_service.refresh_session(refresh_token)
                await session.commit()

            except CantRevokeAlreadyRevokedSession as error:
                await session.commit()
                raise BadRequestError("Сессия уже была отозвана") from error

    except SignatureIsBroken as error:
        raise UnprocessableEntityError("Сигнатура токена повреждена") from error

    except TokenHasExpired as error:
        raise UnprocessableEntityError("Время жизни токена истекло") from error

    set_refresh_in_cookies(response, refresh, secret=jwt_settings.secret.get_secret_value())

    return AccessTokenOut.from_model(access, secret=jwt_settings.secret.get_secret_value())


@router.post(
    "/register-parent",
    summary="Регистрация родителя",
    status_code=status.HTTP_201_CREATED,
    responses=responses.BAD_REQUEST,
)
async def register_parent(session: SessionDep, form: ParentRegistrationForm, user_service: UserServiceDep) -> OKSchema:
    try:
        async with session.begin():
            await user_service.register_parent(
                first_name=form.first_name,
                last_name=form.last_name,
                phone=form.phone,
                email=form.email,
                password=form.password,
            )
            await session.commit()

    except FirstNameContainsNotCyrillicCharacters as error:
        raise BadRequestError("Имя должно содержать только символы кириллицы") from error

    except LastNameContainsNotCyrillicCharacters as error:
        raise BadRequestError("Фамилия должна содержать только символы кириллицы") from error

    except phone.InvalidPhoneFormat as error:
        raise BadRequestError(f"Неверный формат телефона. Ожидался {phone.EXAMPLE}") from error

    except InvalidEmailFormat as error:
        raise BadRequestError("Неверный формат адреса электронной почты") from error

    except passwords.PasswordIsEmpty as error:
        raise BadRequestError("Пароль не может быть пустым") from error

    except passwords.PasswordIsShort as error:
        raise BadRequestError(f"Слишком короткий пароль. Минимальная длина - {passwords.MIN_LENGTH}") from error

    except passwords.PasswordIsLong as error:
        raise BadRequestError(f"Слишком длинный пароль. Максимальная длина - {passwords.MAX_LENGTH}") from error

    except passwords.PasswordDoesntContainUpperLetter as error:
        raise BadRequestError("Пароль должен содержать заглавную букву") from error

    except passwords.PasswordDoesntContainLowerLetter as error:
        raise BadRequestError("Пароль должен содержать строчную букву") from error

    except passwords.PasswordMustContainOnlyASCIILetter as error:
        raise BadRequestError("Пароль должен содержать кириллицу или латиницу") from error

    except passwords.PasswordDoesntContainDigit as error:
        raise BadRequestError("Пароль должен содержать цифру") from error

    except passwords.PasswordMustNotContainSpaces as error:
        raise BadRequestError("Пароль не должен содержать пробелы") from error

    except passwords.PasswordContainsUnavailableSpecialCharacter as error:
        raise BadRequestError("Пароль содержит недопустимые спецсимволы") from error

    except PhoneBelongsToAnotherParent as error:
        raise BadRequestError("Телефон уже привязан к другому родителю") from error

    return OKSchema()


@router.get(
    "/me",
    summary="Получить информацию об пользователе",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND | responses.UNPROCESSABLE_ENTITY,
)
async def get_user_by_access_token(access_token: AccessTokenDep, user_service: UserServiceDep) -> UserOut:
    try:
        user = await user_service.get_user_by_access_token(access_token)

    except SignatureIsBroken as error:
        raise UnprocessableEntityError("Сигнатура токена повреждена") from error

    except TokenHasExpired as error:
        raise UnprocessableEntityError("Время жизни токена истекло") from error

    except NotFoundUser as error:
        raise NotFoundError("Не был найден найден пользователь, для которого был выпущен токен") from error

    return UserOut.from_model(user)
