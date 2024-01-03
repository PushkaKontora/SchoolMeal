from datetime import datetime, timedelta

from app.nutrition.domain.pupil import NutritionStatus, PreferentialCertificate, Pupil


def test_updating_mealtimes(pupil: Pupil):
    pupil.update_mealtimes(has_breakfast=False, has_dinner=False, has_snacks=False)

    assert pupil.has_breakfast is False
    assert pupil.has_dinner is False
    assert pupil.has_breakfast is False


def test_nutrition_status_is_none(pupil: Pupil):
    pupil.has_breakfast = pupil.has_dinner = pupil.has_snacks = False

    assert pupil.nutrition_status is NutritionStatus.NONE


def test_nutrition_status_is_preferential(pupil: Pupil):
    pupil.has_breakfast = True
    pupil.preferential_certificate = PreferentialCertificate(ends_at=datetime.now() + timedelta(days=10))

    assert pupil.nutrition_status is NutritionStatus.PREFERENTIAL


def test_nutrition_status_is_none_when_certificate_was_attached(pupil: Pupil):
    pupil.has_breakfast = pupil.has_dinner = pupil.has_snacks = False
    pupil.preferential_certificate = PreferentialCertificate(ends_at=datetime.now() + timedelta(days=10))

    assert pupil.nutrition_status is NutritionStatus.NONE


def test_nutrition_status_is_paid_when_certificate_is_expired(pupil: Pupil):
    pupil.has_breakfast = True
    pupil.preferential_certificate = PreferentialCertificate(ends_at=datetime.now() - timedelta(days=10))

    assert pupil.nutrition_status is NutritionStatus.PAID
