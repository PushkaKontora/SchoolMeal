from enum import Enum, unique

from pydantic import BaseModel

from app.nutrition.api import dto as nutrition_dto, handlers as nutrition_api
from app.structure.api import dto as structure_dto, handlers as structure_api


@unique
class NutritionSummaryOut(str, Enum):
    NO_EATING = "no_eating"
    PAID = "paid"
    PREFERENTIAL = "preferential"

    @classmethod
    def create(cls, pupil: nutrition_dto.PupilOut) -> "NutritionSummaryOut":
        if not pupil.mealtimes:
            return cls.NO_EATING

        return {
            nutrition_dto.NutritionStatusOut.PAID: cls.PAID,
            nutrition_dto.NutritionStatusOut.PREFERENTIAL: cls.PREFERENTIAL,
        }[pupil.nutrition]


class ChildSummaryOut(BaseModel):
    id: str
    last_name: str
    first_name: str
    school: structure_dto.SchoolOut
    school_class: structure_dto.SchoolClassOut
    status: NutritionSummaryOut | None

    @classmethod
    def create_many(
        cls,
        pupils: list[structure_dto.PupilOut],
        meals: list[nutrition_api.PupilOut],
        school: structure_dto.SchoolOut,
        classes: list[structure_api.SchoolClassOut],
    ) -> "list[ChildSummaryOut]":
        nutrition_by_id = {x.id: x for x in meals}
        class_by_id = {x.id: x for x in classes}

        result: list[ChildSummaryOut] = []

        for pupil in pupils:
            nutrition, school_class_out = nutrition_by_id.get(pupil.id), class_by_id[pupil.class_id]

            result.append(
                ChildSummaryOut(
                    id=pupil.id,
                    last_name=pupil.name.last,
                    first_name=pupil.name.first,
                    school=school,
                    school_class=school_class_out,
                    status=NutritionSummaryOut.create(nutrition) if nutrition else None,
                )
            )

        return result
