from pydantic import BaseModel


class AccessTokenOut(BaseModel):
    token: str
