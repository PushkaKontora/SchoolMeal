from typing import Annotated

from fastapi import Depends, Header

from app.common.domain.authenticated_user import AuthenticatedUser


def _get_authenticated_user(
    x_user: str = Header(alias="X-User", example={"id": "844c4372-52eb-4452-b314-728583ee5fbf", "role": "parent"})
) -> AuthenticatedUser:
    return AuthenticatedUser.parse_raw(x_user)


AuthenticatedUserDep = Annotated[AuthenticatedUser, Depends(_get_authenticated_user)]
