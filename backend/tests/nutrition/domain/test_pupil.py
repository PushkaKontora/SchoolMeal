from datetime import datetime, timedelta

from app.nutrition.domain.pupil import MealPlan, NutritionStatus, PreferentialCertificate, Pupil


def test_nutrition_status_is_none(pupil: Pupil):
    pupil.update_meal_plan(MealPlan(False, False, False))

    assert pupil.nutrition_status is NutritionStatus.NONE


def test_nutrition_status_is_preferential(pupil: Pupil):
    pupil.update_meal_plan(MealPlan(True, False, False))
    pupil.preferential_certificate = PreferentialCertificate(ends_at=datetime.now() + timedelta(days=10))

    assert pupil.nutrition_status is NutritionStatus.PREFERENTIAL


def test_nutrition_status_is_none_when_certificate_was_attached(pupil: Pupil):
    pupil.update_meal_plan(MealPlan(False, False, False))
    pupil.preferential_certificate = PreferentialCertificate(ends_at=datetime.now() + timedelta(days=10))

    assert pupil.nutrition_status is NutritionStatus.NONE


def test_nutrition_status_is_paid_when_certificate_is_expired(pupil: Pupil):
    pupil.update_meal_plan(MealPlan(True, False, False))
    pupil.preferential_certificate = PreferentialCertificate(ends_at=datetime.now() - timedelta(days=10))

    assert pupil.nutrition_status is NutritionStatus.PAID
