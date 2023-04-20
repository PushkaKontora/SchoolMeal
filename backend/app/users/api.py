from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory, List

from app.auth.domain.services import PasswordService
from app.auth.presentation.middlewares import JWTAuth
from app.users.domain.services import UserService
from app.users.presentation.handlers import (
    MeHandlers,
    NonUniqueUserDataHandler,
    NotFoundUserByTokenHandler,
    UsersHandlers,
)
from app.users.presentation.routers import MeRouter, UsersRouter


class UsersAPI(DeclarativeContainer):
    jwt_auth = Dependency(instance_of=JWTAuth)
    password_service = Dependency(instance_of=PasswordService)

    user_service = Factory(UserService, password_service=password_service)

    users_handlers = Factory(UsersHandlers, user_service=user_service)
    me_handlers = Factory(MeHandlers, user_service=user_service)

    exceptions_handlers = List(
        Factory(NonUniqueUserDataHandler),
        Factory(NotFoundUserByTokenHandler),
    )

    me_router = Factory(MeRouter, me_handlers=me_handlers, jwt_auth=jwt_auth)
    router = Factory(UsersRouter, users_handlers=users_handlers, me_router=me_router)
