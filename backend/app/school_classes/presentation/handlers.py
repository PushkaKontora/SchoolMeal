from fastapi import Depends

from app.school_classes.domain.entities import ClassOut, SchoolClassesGetOptions
from app.school_classes.domain.services import get_school_classes_by_options


async def get_school_classes(options: SchoolClassesGetOptions = Depends()) -> list[ClassOut]:
    return await get_school_classes_by_options(options)
