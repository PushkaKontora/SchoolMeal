from dataclasses import dataclass
from ipaddress import IPv4Address

from app.user.application.repositories import IUserRepository
from app.user.domain.model import Email, FirstName, LastName, Login, Password, Phone, RefreshToken, Tokens, User


@dataclass
class UserService:
    user_repository: IUserRepository

    async def authenticate(self, login: str, password: str, ip: IPv4Address) -> Tokens:
        """
        Аутентификация по логину и паролю

        :raise EmptyLoginError: логин не содержит символов
        :raise EmptyPasswordError: пароль не содержит символов
        :raise NotFoundUserError: пользователь с заданным логином не найден
        :raise NotVerifiedPasswordError: пароль не совпадает
        """

        user = await self.user_repository.get_by_login(login=Login(login))

        tokens = user.authenticate(password=Password(password), ip=ip)

        await self.user_repository.update_refresh_tokens_at(user)

        return tokens

    async def reissue_tokens(self, refresh_token: str, ip: IPv4Address) -> Tokens:
        """
        Создание новой пары токенов

        :raise InvalidTokenError: невалидный токен или его тип
        :raise NotFoundUserError: не найден пользователь, для которого сгенерирован данный токен
        :raise RevokedTokenError: токен уже был отозван
        :raise TokenExpirationError: токен протух
        """

        decoded_refresh_token = RefreshToken.decode(refresh_token)

        user = await self.user_repository.get_by_id(decoded_refresh_token.user_id)
        tokens = user.reissue_tokens_for(decoded_refresh_token, ip)

        await self.user_repository.update_refresh_tokens_at(user)

        return tokens

    async def register_parent(self, phone: str, password: str, first_name: str, last_name: str, email: str) -> User:
        """
        Регистрация родителя

        :raise InvalidPhoneFormatError: невалидный формат номера телефона
        :raise EmptyPasswordError: пароль не содержит символов
        :raise EmptyFirstNameError: имя не содержит символов
        :raise EmptyLastNameError: фамилия не содержит символов
        :raise InvalidEmailFormatError: невалидный формат электронной почты
        :raise NotUniqueUserDataError: неуникальные логин, телефон или почта
        """

        user = User.create_parent(
            phone=Phone(phone),
            password=Password(password).hash(),
            first_name=FirstName(first_name),
            last_name=LastName(last_name),
            email=Email(email),
        )

        await self.user_repository.save(user)

        return user
