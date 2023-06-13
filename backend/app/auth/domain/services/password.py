import bcrypt
from dependency_injector.wiring import Provide

from app.appcontainer import AppContainer
from app.config import PasswordSettings


def check_password(
    password: str, hashed_password: bytes, settings: PasswordSettings = Provide[AppContainer.password_settings]
) -> bool:
    return bcrypt.checkpw(password.encode(settings.encoding), hashed_password)


def make_password(password: str, settings: PasswordSettings = Provide[AppContainer.password_settings]) -> bytes:
    salt = bcrypt.gensalt(settings.rounds)

    return bcrypt.hashpw(password.encode(settings.encoding), salt)
