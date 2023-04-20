from fastapi import Request

from app.exceptions import ExceptionHandler
from app.users.domain.entities import ProfileOut, RegistrationSchema
from app.users.domain.exceptions import NonUniqueUserDataException, NotFoundUserByTokenException
from app.users.domain.services import UserService


class UsersHandlers:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    async def register_parent(self, form: RegistrationSchema) -> ProfileOut:
        return await self._user_service.register_parent(
            form.phone, form.password, form.last_name, form.first_name, form.email
        )


class MeHandlers:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    async def get_user_profile_by_token(self, request: Request) -> ProfileOut:
        return await self._user_service.get_user_profile_by_token(request.payload)


class NonUniqueUserDataHandler(ExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return NonUniqueUserDataException

    @property
    def message(self) -> str:
        return "Login, phone or email should be unique"


class NotFoundUserByTokenHandler(ExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return NotFoundUserByTokenException

    @property
    def message(self) -> str:
        return "Not found user"

    @property
    def status_code(self) -> int:
        return 404
