from fastapi import APIRouter

from app.common.api.errors import NotFoundError
from app.common.api.schemas import HTTPError
from app.users.api.dependencies.repositories import UsersRepositoryDep
from app.users.api.dependencies.tokens import AccessTokenDep
from app.users.api.user.schemas import UserOut
from app.users.application.repositories import NotFoundUserError
from app.users.application.use_cases.user import get_user_by_access_token


router = APIRouter()


@router.get(
    "/me",
    summary="Получить информацию об пользователе",
    status_code=200,
    responses={404: {"model": HTTPError}},
)
async def get_user_by_access_token_(access_token: AccessTokenDep, users_repository: UsersRepositoryDep) -> UserOut:
    try:
        user = await get_user_by_access_token(access_token, users_repository)

    except NotFoundUserError as error:
        raise NotFoundError(detail="Пользователь не был найден") from error

    return UserOut.from_model(user)
