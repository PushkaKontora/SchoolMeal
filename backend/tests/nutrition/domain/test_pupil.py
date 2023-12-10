import itertools
from datetime import datetime, timedelta, timezone

import pytest

from app.nutrition.domain.certificate import PreferentialCertificate
from app.nutrition.domain.meal_plan import MealPlan
from app.nutrition.domain.pupil import CantAttachExpiredPreferentialCertificate, MealStatus, Pupil


def test_updating_meal_plan(pupil: Pupil, new_plan: MealPlan):
    pupil.update_meal_plan(new_plan)
    assert pupil.meal_plan == new_plan


def test_attaching_preferential_certificate(pupil: Pupil, certificate: PreferentialCertificate):
    pupil.attach_preferential_certificate(certificate)
    assert pupil.preferential_certificate == certificate


def test_attaching_expired_preferential_certificate(pupil: Pupil):
    pupil.detach_preferential_certificate()

    certificate = PreferentialCertificate((datetime.now(timezone.utc) - timedelta(days=30)).date())

    with pytest.raises(CantAttachExpiredPreferentialCertificate):
        pupil.attach_preferential_certificate(certificate)

    assert pupil.preferential_certificate is None


def test_none_meal_status(pupil: Pupil, certificate: PreferentialCertificate):
    plan = MealPlan(has_breakfast=False, has_dinner=False, has_snacks=False)
    pupil.update_meal_plan(plan)

    pupil.attach_preferential_certificate(certificate)
    assert pupil.status == MealStatus.NONE

    pupil.detach_preferential_certificate()
    assert pupil.status == MealStatus.NONE


@pytest.mark.parametrize(["has_breakfast", "has_dinner", "has_snacks"], itertools.product([False, True], repeat=3))
def test_paid_meal_status(pupil: Pupil, has_breakfast: bool, has_dinner: bool, has_snacks: bool):
    pupil.update_meal_plan(plan=MealPlan(has_breakfast, has_dinner, has_snacks))
    pupil.detach_preferential_certificate()

    if not has_breakfast and not has_dinner and not has_snacks:
        assert pupil.status == MealStatus.NONE
    else:
        assert pupil.status == MealStatus.PAID


@pytest.mark.parametrize(["has_breakfast", "has_dinner", "has_snacks"], itertools.product([False, True], repeat=3))
def test_preferential_meal_status(
    pupil: Pupil, certificate: PreferentialCertificate, has_breakfast: bool, has_dinner: bool, has_snacks: bool
):
    plan = MealPlan(has_breakfast, has_dinner, has_snacks)
    pupil.update_meal_plan(plan)

    pupil.attach_preferential_certificate(certificate)

    if plan == MealPlan(has_breakfast=False, has_dinner=False, has_snacks=False):
        assert pupil.status == MealStatus.NONE
    else:
        assert pupil.status == MealStatus.PREFERENTIAL


@pytest.fixture
def certificate() -> PreferentialCertificate:
    return PreferentialCertificate((datetime.now(timezone.utc) + timedelta(days=30)).date())
