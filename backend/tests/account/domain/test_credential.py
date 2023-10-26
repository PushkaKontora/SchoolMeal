from uuid import uuid4

import pytest

from app.account.domain.credential import Credential, IncorrectPasswordError
from app.account.domain.login import Login
from app.account.domain.passwords import Password


def test_authenticate(credential: Credential):
    authenticated = credential.authenticate(Password("1234"))

    assert authenticated.id == credential.id
    assert authenticated.login == credential.login
    assert authenticated.password == credential.password


def test_authenticated_using_incorrect_password(credential: Credential):
    with pytest.raises(IncorrectPasswordError):
        credential.authenticate(Password("incorrect_password"))


@pytest.fixture(scope="module")
def credential() -> Credential:
    return Credential(
        id=uuid4(),
        login=Login("username"),
        password=Password("1234").hash(),
    )
