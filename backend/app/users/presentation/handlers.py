from fastapi import Body, Depends

from app.auth.domain.entities import JWTPayload
from app.auth.presentation.dependencies import JWTAuth
from app.users.domain.entities import ProfileOut, RegistrationSchema
from app.users.domain.services import get_profile_by_access_token_payload, register_parent as register_parent_


async def register_parent(form: RegistrationSchema = Body()) -> ProfileOut:
    return await register_parent_(form)


async def get_profile(payload: JWTPayload = Depends(JWTAuth())) -> ProfileOut:
    return await get_profile_by_access_token_payload(payload)
