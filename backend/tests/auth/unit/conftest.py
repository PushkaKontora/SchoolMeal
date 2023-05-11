import pytest

from app.auth.presentation.middlewares import JWTAuth


@pytest.fixture
def jwt_auth() -> JWTAuth:
    return JWTAuth()
