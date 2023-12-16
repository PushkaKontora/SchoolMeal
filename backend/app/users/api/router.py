from fastapi import APIRouter, Response, status

from app.shared.fastapi import responses
from app.shared.fastapi.errors import AuthorizationError, BadRequestError, NotFoundError, UnprocessableEntityError
from app.shared.fastapi.schemas import AuthorizedUser, OKSchema
from app.users.api.dependencies.services import UsersServiceDep
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
from app.users.domain.session import SessionIsAlreadyRevoked
from app.users.domain.tokens import SignatureIsBroken, TokenHasExpired


router = APIRouter(prefix="/users", tags=["Аутентификация и пользователи"])


@router.get(
    "/authorize",
    summary="Авторизация для обращения к эндпоинтам",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=responses.FORBIDDEN,
)
async def authorize(access_token: AccessTokenDep, users_service: UsersServiceDep) -> Response:
    try:
        user = await users_service.authorize(access_token)
    except Exception as error:
        raise AuthorizationError from error

    user_out = AuthorizedUser(
        id=user.id,
        role=user.role.value,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT, headers={"X-User": user_out.json()})


@router.post(
    "/authenticate",
    summary="Аутентификация по логину и паролю",
    status_code=status.HTTP_200_OK,
    responses=responses.BAD_REQUEST | responses.UNPROCESSABLE_ENTITY,
)
async def authenticate(
    response: Response,
    credential: CredentialIn,
    user_service: UsersServiceDep,
    jwt_settings: JWTSettingsDep,
) -> AccessTokenOut:
    try:
        access_token, refresh_token = await user_service.authenticate(
            login=credential.login,
            password=credential.password,
        )

    except IncorrectLoginOrPassword as error:
        raise BadRequestError("Неверный логин или пароль") from error

    set_refresh_in_cookies(response, refresh_token, settings=jwt_settings)

    return AccessTokenOut.from_model(access_token, settings=jwt_settings)


@router.post(
    "/logout", summary="Выход из аккаунта", status_code=status.HTTP_200_OK, responses=responses.UNPROCESSABLE_ENTITY
)
async def logout(
    response: Response,
    access_token: AccessTokenDep,
    users_service: UsersServiceDep,
) -> OKSchema:
    try:
        await users_service.logout(access_token)

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
    refresh_token: RefreshTokenDep,
    users_service: UsersServiceDep,
    jwt_settings: JWTSettingsDep,
) -> AccessTokenOut:
    try:
        access, refresh = await users_service.refresh_session(refresh_token)

    except SessionIsAlreadyRevoked as error:
        raise BadRequestError("Сессия уже была отозвана") from error

    except SignatureIsBroken as error:
        raise UnprocessableEntityError("Сигнатура токена повреждена") from error

    except TokenHasExpired as error:
        raise UnprocessableEntityError("Время жизни токена истекло") from error

    set_refresh_in_cookies(response, refresh, settings=jwt_settings)

    return AccessTokenOut.from_model(access, settings=jwt_settings)


@router.post(
    "/register-parent",
    summary="Регистрация родителя",
    status_code=status.HTTP_201_CREATED,
    responses=responses.BAD_REQUEST,
)
async def register_parent(form: ParentRegistrationForm, users_service: UsersServiceDep) -> OKSchema:
    try:
        await users_service.register_parent(
            first_name=form.first_name,
            last_name=form.last_name,
            phone=form.phone,
            email=form.email,
            password=form.password,
        )

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
async def get_user_by_access_token(access_token: AccessTokenDep, users_service: UsersServiceDep) -> UserOut:
    try:
        user = await users_service.get_user_by_access_token(access_token)

    except SignatureIsBroken as error:
        raise UnprocessableEntityError("Сигнатура токена повреждена") from error

    except TokenHasExpired as error:
        raise UnprocessableEntityError("Время жизни токена истекло") from error

    except NotFoundUser as error:
        raise NotFoundError("Не был найден найден пользователь, для которого был выпущен токен") from error

    return UserOut.from_model(user)
