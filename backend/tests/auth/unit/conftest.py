import pytest

from app.auth.api import AuthAPI
from app.auth.presentation.middlewares import JWTAuth


@pytest.fixture(scope="session")
def container() -> AuthAPI:
    return AuthAPI()


@pytest.fixture
def jwt_auth(container: AuthAPI) -> JWTAuth:
    return container.jwt_auth()
