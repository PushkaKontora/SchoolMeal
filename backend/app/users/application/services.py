from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.shared.unit_of_work import UnitOfWork
from app.users.application.repositories import ISessionsRepository, IUsersRepository, NotFoundUser, NotUniqueLogin
from app.users.domain.email import Email
from app.users.domain.login import Login
from app.users.domain.names import FirstName, LastName
from app.users.domain.passwords import Password, StrictPassword
from app.users.domain.phone import Phone
from app.users.domain.session import CantRevokeAlreadyRevokedSession, Session
from app.users.domain.tokens import AccessToken, RefreshToken
from app.users.domain.user import PasswordIsNotVerified, User


class IncorrectLoginOrPassword(Exception):
    pass


class PhoneBelongsToAnotherParent(Exception):
    pass


class UsersService:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        users_repository: IUsersRepository,
        sessions_service: "SessionsService",
        secret: str,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._users = users_repository

        self._sessions_service = sessions_service

        self._secret = secret

    async def authenticate(self, login: str, password: str) -> tuple[AccessToken, RefreshToken]:
        """
        :raise IncorrectLoginOrPassword: неверный логин или пароль
        """

        async with self._unit_of_work as session:
            try:
                user = await self._users.get_by_login(login=Login(login))
                authenticated_user = user.authenticate(password=Password(password))

            except (NotFoundUser, PasswordIsNotVerified) as error:
                raise IncorrectLoginOrPassword from error

            tokens = await self._sessions_service.open_session(user_id=authenticated_user.id, device_id=uuid4())
            await session.commit()

        return tokens

    async def logout(self, access_token: str) -> None:
        """
        :raise SignatureIsBroken: токен повреждён
        :raise TokenHasExpired: время жизни токена истекло
        """

        async with self._unit_of_work as session:
            token = AccessToken.decode(access_token, secret=self._secret)

            await self._sessions_service.revoke_all_session_on_device_belonging_to_user(
                user_id=token.user_id, device_id=token.device_id
            )

            await session.commit()

    async def get_user_by_access_token(self, access_token: str) -> User:
        """
        :raise SignatureIsBroken: токен повреждён
        :raise TokenHasExpired: время жизни токена истекло
        :raise NotFoundUser: не был найден пользователь, для которого был выпущен токен
        """

        token = AccessToken.decode(access_token, secret=self._secret)

        return await self._users.get_by_id(user_id=token.user_id)

    async def register_parent(
        self,
        first_name: str,
        last_name: str,
        phone: str,
        email: str,
        password: str,
    ) -> User:
        """
        :raise FirstNameContainsNotCyrillicCharacters: имя содержит не кириллицу
        :raise LastNameContainsNotCyrillicCharacters: фамилия содержит не кириллицу
        :raise InvalidPhoneFormat: неверный формат телефона
        :raise InvalidEmailFormat: неверный формат адреса электронной почты
        :raise PasswordIsEmpty: пароль пустой
        :raise PasswordIsShort: короткий пароль
        :raise PasswordIsLong: длинный пароль
        :raise PasswordDoesntContainUpperLetter: пароль не содержит заглавную букву
        :raise PasswordDoesntContainLowerLetter: пароль не содержит строчную букву
        :raise PasswordMustContainOnlyASCIILetter: пароль должен содержать кириллицу или латиницу
        :raise PasswordDoesntContainDigit: пароль не содержит цифру
        :raise PasswordMustNotContainSpaces: пароль содержит пробел
        :raise PasswordContainsUnavailableSpecialCharacter: пароль содержит запрещённый символ пунктуации
        :raise PhoneBelongsToAnotherParent: телефон принадлежит другому родителю
        """

        async with self._unit_of_work as session:
            parent = User.create_parent(
                first_name=FirstName(first_name),
                last_name=LastName(last_name),
                phone=Phone(phone),
                email=Email(email),
                password=StrictPassword(password),
            )

            try:
                await self._users.save(parent)
            except NotUniqueLogin as error:
                raise PhoneBelongsToAnotherParent from error

            await session.commit()

        return parent

    async def authorize(self, access_token: str) -> User:
        """
        :raise SignatureIsBroken: токен повреждён
        :raise TokenHasExpired: время жизни токена истекло
        :raise NotFoundUser: не был найден пользователь, для которого был выпущен токен
        """

        # TODO: переписать временную заглушку https://miro.com/app/board/uXjVMqgVYdU=/?moveToWidget=3458764569629152407&cot=14
        return await self.get_user_by_access_token(access_token)


@dataclass
class SessionsService:
    def __init__(self, unit_of_work: UnitOfWork, sessions_repository: ISessionsRepository, secret: str) -> None:
        self._unit_of_work = unit_of_work
        self._sessions = sessions_repository
        self._secret = secret

    async def open_session(self, user_id: UUID, device_id: UUID) -> tuple[AccessToken, RefreshToken]:
        async with self._unit_of_work as app_session:
            refresh = RefreshToken(jti=uuid4(), device_id=device_id, user_id=user_id, iat=datetime.now(tz=timezone.utc))
            access = AccessToken(jti=uuid4(), device_id=device_id, user_id=user_id, iat=datetime.now(tz=timezone.utc))

            session = Session(
                id=uuid4(),
                jti=refresh.jti,
                user_id=user_id,
                device_id=device_id,
                revoked=False,
                created_at=datetime.now(tz=timezone.utc),
            )

            await self._sessions.save(session)
            await app_session.commit()

        return access, refresh

    async def refresh_session(self, refresh_token: str) -> tuple[AccessToken, RefreshToken]:
        """
        :raise SignatureIsBroken: токен повреждён
        :raise TokenHasExpired: время жизни токена истекло
        :raise CantRevokeAlreadyRevokedSession: сессия уже была отозванной
        """

        async with self._unit_of_work as app_session:
            token = RefreshToken.decode(refresh_token, secret=self._secret)
            session = await self._sessions.get_by_jti(jti=token.jti)

            try:
                session.revoke()
                await self._sessions.update(session)

            except CantRevokeAlreadyRevokedSession:
                await self.revoke_all_sessions_belonging_to_user(user_id=session.user_id)
                await app_session.commit()
                raise

            tokens = await self.open_session(user_id=session.user_id, device_id=session.device_id)

            await app_session.commit()

        return tokens

    async def revoke_all_sessions_belonging_to_user(self, user_id: UUID) -> list[Session]:
        async with self._unit_of_work as app_session:
            sessions = await self._sessions.get_all_by_user_id_and_revoked(user_id=user_id, revoked=False)

            for non_revoked_session in sessions:
                non_revoked_session.revoke()

            await self._sessions.update(*sessions)

            await app_session.commit()

        return sessions

    async def revoke_all_session_on_device_belonging_to_user(self, user_id: UUID, device_id: UUID) -> list[Session]:
        async with self._unit_of_work as app_session:
            sessions = await self._sessions.get_all_by_user_id_and_device_id_and_revoked(
                user_id=user_id, device_id=device_id, revoked=False
            )

            for session in sessions:
                session.revoke()

            await self._sessions.update(*sessions)

            await app_session.commit()

        return sessions
