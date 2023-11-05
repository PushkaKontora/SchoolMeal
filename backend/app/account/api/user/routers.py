from fastapi import APIRouter

from app.account.api.dependencies.repositories import UsersRepositoryDep
from app.account.api.dependencies.tokens import AccessTokenDep
from app.account.api.user.schemas import UserOut
from app.account.application.repositories import NotFoundUserError
from app.account.application.use_cases.user import get_user_by_access
from app.common.api.errors import NotFoundError
from app.common.api.schemas import HTTPError


router = APIRouter()


@router.get(
    "/me",
    summary="Получить информацию об аккаунте",
    status_code=200,
    responses={404: {"model": HTTPError}},
)
async def get_account_info_by_access_token(access: AccessTokenDep, users_repository: UsersRepositoryDep) -> UserOut:
    try:
        user = await get_user_by_access(access, users_repository)

    except NotFoundUserError as error:
        raise NotFoundError(detail="Аккаунт не был найден") from error

    return UserOut.from_model(user)
