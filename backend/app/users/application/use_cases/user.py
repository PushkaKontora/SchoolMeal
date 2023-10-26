from app.users.application.repositories import IUsersRepository
from app.users.domain.tokens import AccessToken
from app.users.domain.user import User


async def get_user_by_access_token(access_token: AccessToken, users_repository: IUsersRepository) -> User:
    """
    :raise NotFoundUserError: пользователь не найден
    """

    return await users_repository.get_by_id(user_id=access_token.user_id)
