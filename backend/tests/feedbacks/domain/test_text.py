import pytest

from app.feedbacks.domain.feedback import FeedbackText


def test_empty_text() -> None:
    with pytest.raises(ValueError) as error:
        FeedbackText("")

    assert str(error.value) == "Текст не должен быть пустым"


@pytest.mark.parametrize("length", [1, 255])
def test_correct_text(length: int) -> None:
    expected = "a" * length
    text = FeedbackText(expected)

    assert text.value == expected


def test_big_text() -> None:
    with pytest.raises(ValueError) as error:
        FeedbackText("a" * 256)

    assert str(error.value) == "Текст отзыва превысил допустимую длину - 255 символов"
