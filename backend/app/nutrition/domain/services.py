from app.nutrition.domain.request import DraftRequest, PupilInfo, Request
from app.nutrition.domain.school_class import SchoolClass


class DraftDoesNotBelongToClass(Exception):
    pass


def submit_request(school_class: SchoolClass, draft: DraftRequest) -> Request:
    """
    :raise DraftDoesNotBelongToClass: черновик создан не для этого класса
    """

    if draft and draft.class_id != school_class.id:
        raise DraftDoesNotBelongToClass

    return Request(
        class_id=school_class.id,
        on_date=draft.on_date,
        pupils=[
            PupilInfo(
                id=pupil.id, plan=draft.pupils.get(pupil.id) or pupil.meal_plan, preferential=pupil.is_preferential
            )
            for pupil in school_class.pupils
        ],
    )
