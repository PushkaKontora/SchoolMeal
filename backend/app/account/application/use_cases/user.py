from app.account.application.repositories import IUsersRepository
from app.account.domain.tokens import AccessToken
from app.account.domain.user import User


async def get_user_by_access(access: AccessToken, users_repository: IUsersRepository) -> User:
    """
    :raise NotFoundUserError: пользователь не найден
    """

    return await users_repository.get_by_credential_id(credential_id=access.credential_id)
