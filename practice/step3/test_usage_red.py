"""Các test đỏ của bài 3. Đọc log rồi quyết định sửa cái gì."""

import pytest

from gas.reading import usage_between


@pytest.fixture
def previous() -> int:
    return 1200


def test_meter_goes_back_to_0_after_9999() -> None:
    assert usage_between(9998, 3) == 5


def test_usage_is_current_minus_previous() -> None:
    assert usage_between(1200, 1230) == 31


def test_usage_for_a_small_month(previous_reading: int) -> None:
    assert usage_between(previous_reading, previous_reading + 5) == 5
