import bcrypt
from dependency_injector.wiring import Provide

from app.config import PasswordSettings
from app.container import Container


def check_password(
    password: str, hashed_password: bytes, settings: PasswordSettings = Provide[Container.password_settings]
) -> bool:
    return bcrypt.checkpw(password.encode(settings.encoding), hashed_password)


def make_password(password: str, settings: PasswordSettings = Provide[Container.password_settings]) -> bytes:
    salt = bcrypt.gensalt(settings.rounds)

    return bcrypt.hashpw(password.encode(settings.encoding), salt)
