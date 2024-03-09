from datetime import date
from typing import Iterable

from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import Pupil, PupilID
from app.nutrition.domain.request import Declaration, Request, RequestStatus
from app.nutrition.domain.school_class import SchoolClass
from app.nutrition.domain.time import Day


def prefill_request(
    school_class: SchoolClass, pupils: Iterable[Pupil], on_date: date, overrides: dict[PupilID, set[Mealtime]]
) -> Request:
    declarations: set[Declaration] = set()

    for pupil in pupils:
        if pupil.class_id != school_class.id:
            raise ValueError(f"Ученик id={pupil.id} не принадлежит классу id={school_class.id}")

        mealtimes: set[Mealtime] = set()
        for mealtime in school_class.mealtimes:
            eats = pupil.does_eat(day=Day(on_date), mealtime=mealtime)

            if pupil.id in overrides:
                eats = mealtime in overrides[pupil.id]

            if eats:
                mealtimes.add(mealtime)

        declarations.add(Declaration(pupil_id=pupil.id, mealtimes=mealtimes, nutrition=pupil.nutrition))

    return Request(
        class_id=school_class.id,
        on_date=on_date,
        mealtimes=school_class.mealtimes,
        declarations=declarations,
        status=RequestStatus.PREFILLED,
    )
