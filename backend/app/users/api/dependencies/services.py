from typing import Annotated

from fastapi import Depends

from app.users.api.dependencies.repositories import SessionsRepositoryDep, UsersRepositoryDep
from app.users.api.dependencies.settings import JWTSettingsDep
from app.users.application.services import SessionService, UserService


def _get_session_service(sessions_repository: SessionsRepositoryDep, jwt_settings: JWTSettingsDep) -> SessionService:
    return SessionService(repository=sessions_repository, secret=jwt_settings.secret.get_secret_value())


def _get_user_service(
    users_repository: UsersRepositoryDep, session_service: "SessionServiceDep", jwt_settings: JWTSettingsDep
) -> UserService:
    return UserService(
        repository=users_repository, session_service=session_service, secret=jwt_settings.secret.get_secret_value()
    )


SessionServiceDep = Annotated[SessionService, Depends(_get_session_service)]
UserServiceDep = Annotated[UserService, Depends(_get_user_service)]
