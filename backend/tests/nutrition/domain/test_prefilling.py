from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import Pupil
from app.nutrition.domain.school_class import SchoolClass
from app.nutrition.domain.services import prefill_request
from app.nutrition.domain.time import now


def test_without_overriding(school_class: SchoolClass, pupil: Pupil) -> None:
    request = prefill_request(school_class, [pupil], on_date=now().date(), overrides={})

    assert len(request.declarations) == 1

    declaration = next(iter(request.declarations))
    assert declaration.pupil_id == pupil.id
    assert declaration.mealtimes == pupil.mealtimes


def test_with_overriding(school_class: SchoolClass, pupil: Pupil) -> None:
    resumed = {Mealtime.DINNER, Mealtime.SNACKS, Mealtime.BREAKFAST}

    request = prefill_request(school_class, [pupil], on_date=now().date(), overrides={pupil.id: resumed})

    assert len(request.declarations) == 1

    declaration = next(iter(request.declarations))
    assert declaration.pupil_id == pupil.id
    assert declaration.mealtimes == resumed & school_class.mealtimes
