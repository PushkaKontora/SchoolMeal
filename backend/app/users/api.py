from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory, List

from app.auth.domain.services import PasswordService
from app.users.domain.services import UserService
from app.users.presentation.handlers import NonUniqueUserDataHandler, UsersHandlers
from app.users.presentation.routers import UsersRouter


class UsersAPI(DeclarativeContainer):
    password_service = Dependency(instance_of=PasswordService)

    user_service = Factory(UserService, password_service=password_service)

    users_handlers = Factory(UsersHandlers, user_service=user_service)

    exceptions_handlers = List(
        Factory(NonUniqueUserDataHandler),
    )

    router = Factory(UsersRouter, users_handlers=users_handlers)
