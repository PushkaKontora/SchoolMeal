from typing import Annotated

from fastapi import Depends

from app.db.settings import DatabaseSettings


DatabaseSettingsDep = Annotated[DatabaseSettings, Depends(lambda: DatabaseSettings(), use_cache=True)]
