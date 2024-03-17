from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.gateway.web.v1.school_classes.dto import GetSchoolClassesParams
from app.structure.api import dto as structure_dto, handlers as structure_api


router = APIRouter()


@router.get(
    "/school-classes",
    summary="Получить список классов",
    status_code=status.HTTP_200_OK,
)
async def get_school_classes(
    params: Annotated[GetSchoolClassesParams, Depends()]
) -> list[structure_dto.SchoolClassOut]:
    return await structure_api.get_classes(filters=structure_dto.ClassesFilters(teacher_id=params.teacher_id))
