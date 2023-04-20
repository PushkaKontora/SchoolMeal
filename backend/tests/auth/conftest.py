import pytest

from app.config import JWTSettings


@pytest.fixture(scope="session")
def auth_settings() -> JWTSettings:
    return JWTSettings()
