from contextlib import nullcontext

import pytest

from app.feedbacks.domain.text import ExceededMaxLengthFeedbackText, FeedbackText, InsufficientMinLengthFeedbackText


def test_correct_feedback_text():
    text = """
Лучшая столовая.
Большое спасибо Кристине Юрьевне за приятную атмосферу - уют, чистота и приятная обстановка.
С любовью, М
"""

    feedback_text = FeedbackText(text)
    assert feedback_text.value == text


@pytest.mark.parametrize("length", [0, 1, 255, 256])
def test_length_of_feedback_text(length: int):
    error = nullcontext()
    if length > 255:
        error = pytest.raises(ExceededMaxLengthFeedbackText)
    if length == 0:
        error = pytest.raises(InsufficientMinLengthFeedbackText)

    with error:
        FeedbackText("a" * length)
