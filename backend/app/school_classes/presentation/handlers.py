from fastapi import Depends, Path

from app.pupils.domain.entities import PupilOut
from app.pupils.domain.services import get_pupils_by_class_id
from app.school_classes.domain.entities import ClassWithSchoolOut, SchoolClassesGetOptions
from app.school_classes.domain.services import get_school_classes_by_options


async def get_school_classes(options: SchoolClassesGetOptions = Depends()) -> list[ClassWithSchoolOut]:
    return await get_school_classes_by_options(options)


async def get_pupils(class_id: int = Path()) -> list[PupilOut]:
    return await get_pupils_by_class_id(class_id)
