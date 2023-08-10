from dependency_injector.wiring import Provide, inject

from app.legacy.auth.db.password.model import Password
from app.legacy.auth.domain.entities import JWTPayload
from app.legacy.auth.domain.services.password import make_password
from app.legacy.container import AppContainer
from app.legacy.db.unit_of_work import UnitOfWork
from app.legacy.users.db.user.filters import ByEmail, ByLogin, ByPhone, ByUserId
from app.legacy.users.db.user.model import Role, User
from app.legacy.users.domain.entities import ProfileOut, RegistrationSchema
from app.legacy.users.domain.errors import NonUniqueUserDataError, NotFoundUserError


@inject
async def register_parent(
    schema: RegistrationSchema, uow: UnitOfWork = Provide[AppContainer.unit_of_work]
) -> ProfileOut:
    async with uow:
        if await uow.repository(User).exists(ByLogin(schema.phone) | ByPhone(schema.phone) | ByEmail(schema.email)):
            raise NonUniqueUserDataError

        user = User(
            last_name=schema.last_name,
            first_name=schema.first_name,
            login=schema.phone,
            role=Role.PARENT,
            phone=schema.phone,
            email=schema.email,
            photo_path=None,
            passwords=[Password(value=make_password(schema.password))],
        )
        uow.repository(User).save(user)

        await uow.commit()
        await uow.repository(User).refresh(user)

        return ProfileOut.from_orm(user)


@inject
async def get_profile_by_access_token_payload(
    payload: JWTPayload, uow: UnitOfWork = Provide[AppContainer.unit_of_work]
) -> ProfileOut:
    async with uow:
        user = await uow.repository(User).find_first(ByUserId(payload.user_id))

        if not user:
            raise NotFoundUserError

        return ProfileOut.from_orm(user)
