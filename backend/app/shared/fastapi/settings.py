from pydantic import BaseSettings, Field


class FastAPIConfig(BaseSettings):
    show_swagger_ui: bool = Field(default=False, env="SHOW_SWAGGER_UI")
