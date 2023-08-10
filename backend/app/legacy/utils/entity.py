from functools import partial

from pydantic import BaseModel, Field

from app.legacy.utils.string import camelize_snakecase


DatetimeField = partial(Field, example="2023-04-19T21:58:30.912109")


class Entity(BaseModel):
    class Config:
        allow_mutation = False
        alias_generator = camelize_snakecase
        allow_population_by_field_name = True
        orm_mode = True
