from dependency_injector.wiring import Provide, inject

from app.auth.db.password.model import Password
from app.auth.domain.entities import JWTPayload
from app.auth.domain.services import PasswordService
from app.database.container import Database
from app.database.unit_of_work import UnitOfWork
from app.users.db.user.filters import ByEmail, ById, ByLogin, ByPhone
from app.users.db.user.model import Role, User
from app.users.domain.base_repositories import BaseUsersRepository
from app.users.domain.entities import ProfileOut
from app.users.domain.exceptions import NonUniqueUserDataException, NotFoundUserByTokenException


class UserService:
    def __init__(self, password_service: PasswordService):
        self._password_service = password_service

    @inject
    async def register_parent(
        self,
        phone: str,
        password: str,
        last_name: str,
        first_name: str,
        email: str,
        uow: UnitOfWork = Provide[Database.unit_of_work],
    ) -> ProfileOut:
        async with uow:
            if await uow.users_repo.exists(ByLogin(phone) | ByPhone(phone) | ByEmail(email)):
                raise NonUniqueUserDataException

            user = User(
                last_name=last_name,
                first_name=first_name,
                login=phone,
                role=Role.PARENT,
                phone=phone,
                email=email,
                photo_path=None,
                passwords=[Password(value=self._password_service.make_password(password))],
            )
            uow.users_repo.save(user)

            await uow.commit()
            await uow.users_repo.refresh(user)

            return ProfileOut.from_orm(user)

    @inject
    async def get_user_profile_by_token(
        self, payload: JWTPayload, users_repo: BaseUsersRepository = Provide[Database.users_repository]
    ) -> ProfileOut:
        user = await users_repo.find_one(ById(payload.user_id))

        if not user:
            raise NotFoundUserByTokenException

        return ProfileOut.from_orm(user)
