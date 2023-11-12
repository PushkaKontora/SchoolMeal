from typing import Annotated

from fastapi import Depends

from app.common.infrastructure.settings import JWTSettings


def _get_jwt_settings() -> JWTSettings:
    return JWTSettings()


JWTSettingsDep = Annotated[JWTSettings, Depends(_get_jwt_settings, use_cache=True)]
