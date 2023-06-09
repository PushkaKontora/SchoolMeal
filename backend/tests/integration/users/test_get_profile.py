from httpx import AsyncClient, Response

from app.config import JWTSettings
from app.users.db.user.model import Role, User
from tests.integration.auth.conftest import create_access_token
from tests.integration.conftest import BearerAuth
from tests.integration.responses import error
from tests.integration.users.conftest import ME_PREFIX
from tests.integration.utils import datetime_to_str


async def get(client: AsyncClient, token: str) -> Response:
    return await client.get(ME_PREFIX, auth=BearerAuth(token))


async def test_get_me(client: AsyncClient, parent: User, parent_token: str):
    response = await get(client, parent_token)

    assert response.status_code == 200
    assert response.json() == {
        "id": parent.id,
        "lastName": parent.last_name,
        "firstName": parent.first_name,
        "login": parent.login,
        "role": parent.role.value,
        "email": parent.email,
        "phone": parent.phone,
        "photoPath": parent.photo_path,
        "createdAt": datetime_to_str(parent.created_at),
    }


async def test_get_me_by_unknown_user_id(client: AsyncClient, jwt_settings: JWTSettings):
    token = create_access_token(0, Role.PARENT, jwt_settings)

    response = await get(client, token)

    assert response.status_code == 404
    assert response.json() == error("NotFoundUserError", "Not found user")
