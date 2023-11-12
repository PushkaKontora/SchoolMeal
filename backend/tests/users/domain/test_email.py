import pytest

from app.users.domain.email import Email, InvalidEmailFormat


@pytest.mark.parametrize(
    "value",
    [
        "serious_dim@google.com",
        "serious-dim@google.com",
        "serious+dim@google.com",
        "peroovy@gmail.com",
        "a@a",
        "1@1",
    ],
)
def test_email(value: str):
    Email(value)


@pytest.mark.parametrize(
    "value",
    [
        "",
        "@",
        "name@",
        "@dns",
        "with space@google.com",
        "name@google com",
    ],
)
def test_incorrect_email(value: str):
    with pytest.raises(InvalidEmailFormat):
        Email(value)
