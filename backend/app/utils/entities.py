from pydantic import BaseModel

from app.utils.string import camelize_snakecase


class BaseEntity(BaseModel):
    class Config:
        allow_mutation = False
        alias_generator = camelize_snakecase
        allow_population_by_field_name = True
