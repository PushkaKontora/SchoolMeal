from typing import Annotated

from fastapi import Depends, Header

from app.common.api.schemas import AuthorizedUser


def _get_authenticated_user(
    x_user: str = Header(example={"id": "844c4372-52eb-4452-b314-728583ee5fbf", "role": "parent"})
) -> AuthorizedUser:
    return AuthorizedUser.parse_raw(x_user)


AuthorizedUserDep = Annotated[AuthorizedUser, Depends(_get_authenticated_user)]
