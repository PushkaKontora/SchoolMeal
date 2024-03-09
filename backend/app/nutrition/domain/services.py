from datetime import date
from typing import Iterable

from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import Pupil, PupilID
from app.nutrition.domain.request import Request, RequestStatus
from app.nutrition.domain.school_class import SchoolClass
from app.nutrition.domain.time import Day


def prefill_request(
    school_class: SchoolClass, pupils: Iterable[Pupil], on_date: date, overrides: dict[PupilID, set[Mealtime]]
) -> Request:
    day = Day(on_date)
    mealtimes: dict[Mealtime, set[PupilID]] = {mealtime_: set() for mealtime_ in school_class.mealtimes}

    for pupil in pupils:
        if pupil.class_id != school_class.id:
            raise ValueError(f"Ученик id={pupil.id} не принадлежит классу id={school_class.id}")

        for mealtime, request_ in mealtimes.items():
            eats = pupil.does_eat(day, mealtime)

            if pupil.id in overrides:
                eats = mealtime in overrides[pupil.id]

            if eats:
                request_.add(pupil.id)

    return Request(
        class_id=school_class.id,
        on_date=day.value,
        mealtimes=mealtimes,
        status=RequestStatus.PREFILLED,
    )
