from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status

from app.gateway import responses
from app.gateway.errors import BadRequest, Forbidden, NotFound, UnprocessableEntity
from app.shared.fastapi.schemas import AuthorizedUser, OKSchema
from app.users.api.schemas import AccessTokenOut, CredentialIn, ParentRegistrationForm, UserOut
from app.users.api.tokens import AccessTokenDep, RefreshTokenDep, delete_refresh_from_cookies, set_refresh_in_cookies
from app.users.application.repositories import NotFoundUser
from app.users.application.services import IncorrectLoginOrPassword, PhoneBelongsToAnotherParent, UsersService
from app.users.domain import passwords, phone
from app.users.domain.email import InvalidEmailFormat
from app.users.domain.names import FirstNameContainsNotCyrillicCharacters, LastNameContainsNotCyrillicCharacters
from app.users.domain.session import SessionIsAlreadyRevoked
from app.users.domain.tokens import SignatureIsBroken, TokenHasExpired
from app.users.infrastructure.dependencies import UsersContainer


router = APIRouter(prefix="/users", tags=["Аутентификация и пользователи"])


@router.get(
    "/authorize",
    summary="Авторизация для обращения к эндпоинтам",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=responses.FORBIDDEN,
)
@inject
async def authorize(
    access_token: AccessTokenDep, users_service: UsersService = Depends(Provide[UsersContainer.service])
) -> Response:
    try:
        user = await users_service.authorize(access_token)
    except Exception as error:
        raise Forbidden from error

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
@inject
async def authenticate(
    response: Response,
    credential: CredentialIn,
    users_service: UsersService = Depends(Provide[UsersContainer.service]),
    secret: str = Depends(Provide[UsersContainer.jwt_config.secret]),
) -> AccessTokenOut:
    try:
        access_token, refresh_token = await users_service.authenticate(
            login=credential.login,
            password=credential.password,
        )

    except IncorrectLoginOrPassword as error:
        raise BadRequest("Неверный логин или пароль") from error

    set_refresh_in_cookies(response, refresh_token, secret)

    return AccessTokenOut.from_model(access_token, secret)


@router.post(
    "/logout", summary="Выход из аккаунта", status_code=status.HTTP_200_OK, responses=responses.UNPROCESSABLE_ENTITY
)
@inject
async def logout(
    response: Response,
    access_token: AccessTokenDep,
    users_service: UsersService = Depends(Provide[UsersContainer.service]),
) -> OKSchema:
    try:
        await users_service.logout(access_token)

    except SignatureIsBroken as error:
        raise UnprocessableEntity("Сигнатура токена повреждена") from error

    except TokenHasExpired as error:
        raise UnprocessableEntity("Время жизни токена истекло") from error

    delete_refresh_from_cookies(response)

    return OKSchema()


@router.post(
    "/refresh-tokens",
    summary="Перевыпустить токены",
    status_code=status.HTTP_200_OK,
    responses=responses.BAD_REQUEST | responses.UNPROCESSABLE_ENTITY,
)
@inject
async def refresh_tokens(
    response: Response,
    refresh_token: RefreshTokenDep,
    users_service: UsersService = Depends(Provide[UsersContainer.service]),
    secret: str = Depends(Provide[UsersContainer.jwt_config.secret]),
) -> AccessTokenOut:
    try:
        access, refresh = await users_service.refresh_session(refresh_token)

    except SessionIsAlreadyRevoked as error:
        raise BadRequest("Сессия уже была отозвана") from error

    except SignatureIsBroken as error:
        raise UnprocessableEntity("Сигнатура токена повреждена") from error

    except TokenHasExpired as error:
        raise UnprocessableEntity("Время жизни токена истекло") from error

    set_refresh_in_cookies(response, refresh, secret)

    return AccessTokenOut.from_model(access, secret)


@router.post(
    "/register-parent",
    summary="Регистрация родителя",
    status_code=status.HTTP_201_CREATED,
    responses=responses.BAD_REQUEST,
)
@inject
async def register_parent(
    form: ParentRegistrationForm, users_service: UsersService = Depends(Provide[UsersContainer.service])
) -> OKSchema:
    try:
        await users_service.register_parent(
            first_name=form.first_name,
            last_name=form.last_name,
            phone=form.phone,
            email=form.email,
            password=form.password,
        )

    except FirstNameContainsNotCyrillicCharacters as error:
        raise BadRequest("Имя должно содержать только символы кириллицы") from error

    except LastNameContainsNotCyrillicCharacters as error:
        raise BadRequest("Фамилия должна содержать только символы кириллицы") from error

    except phone.InvalidPhoneFormat as error:
        raise BadRequest(f"Неверный формат телефона. Ожидался {phone.EXAMPLE}") from error

    except InvalidEmailFormat as error:
        raise BadRequest("Неверный формат адреса электронной почты") from error

    except passwords.PasswordIsEmpty as error:
        raise BadRequest("Пароль не может быть пустым") from error

    except passwords.PasswordIsShort as error:
        raise BadRequest(f"Слишком короткий пароль. Минимальная длина - {passwords.MIN_LENGTH}") from error

    except passwords.PasswordIsLong as error:
        raise BadRequest(f"Слишком длинный пароль. Максимальная длина - {passwords.MAX_LENGTH}") from error

    except passwords.PasswordDoesntContainUpperLetter as error:
        raise BadRequest("Пароль должен содержать заглавную букву") from error

    except passwords.PasswordDoesntContainLowerLetter as error:
        raise BadRequest("Пароль должен содержать строчную букву") from error

    except passwords.PasswordMustContainOnlyASCIILetter as error:
        raise BadRequest("Пароль должен содержать кириллицу или латиницу") from error

    except passwords.PasswordDoesntContainDigit as error:
        raise BadRequest("Пароль должен содержать цифру") from error

    except passwords.PasswordMustNotContainSpaces as error:
        raise BadRequest("Пароль не должен содержать пробелы") from error

    except passwords.PasswordContainsUnavailableSpecialCharacter as error:
        raise BadRequest("Пароль содержит недопустимые спецсимволы") from error

    except PhoneBelongsToAnotherParent as error:
        raise BadRequest("Телефон уже привязан к другому родителю") from error

    return OKSchema()


@router.get(
    "/me",
    summary="Получить информацию об пользователе",
    status_code=status.HTTP_200_OK,
    responses=responses.NOT_FOUND | responses.UNPROCESSABLE_ENTITY,
)
@inject
async def get_user_by_access_token(
    access_token: AccessTokenDep, users_service: UsersService = Depends(Provide[UsersContainer.service])
) -> UserOut:
    try:
        user = await users_service.get_user_by_access_token(access_token)

    except SignatureIsBroken as error:
        raise UnprocessableEntity("Сигнатура токена повреждена") from error

    except TokenHasExpired as error:
        raise UnprocessableEntity("Время жизни токена истекло") from error

    except NotFoundUser as error:
        raise NotFound("Не был найден найден пользователь, для которого был выпущен токен") from error

    return UserOut.from_model(user)
