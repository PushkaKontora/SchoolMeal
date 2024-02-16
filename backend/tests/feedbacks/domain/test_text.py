import pytest

from app.feedbacks.domain.feedback import FeedbackText
from app.shared.exceptions import DomainException


def test_empty_text() -> None:
    with pytest.raises(DomainException) as error:
        FeedbackText("")

    assert error.value.message == "Текст не должен быть пустым"


@pytest.mark.parametrize("length", [1, 255])
def test_correct_text(length: int) -> None:
    expected = "a" * length
    text = FeedbackText(expected)

    assert text.value == expected


def test_big_text() -> None:
    with pytest.raises(DomainException) as error:
        FeedbackText("a" * 256)

    assert error.value.message == "Текст отзыва превысил допустимую длину - 255 символов"
