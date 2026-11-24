"""Test để làm quen với output của pytest. Có test cố ý fail và test cố ý error."""

from gas.tariff import Tariff, tariff_for


def test_tariff_a_applies_to_10m3() -> None:
    assert tariff_for(10) is Tariff.A


def test_tariff_b_applies_to_30m3() -> None:
    assert tariff_for(30) is Tariff.B


def test_tariff_c_applies_to_100m3() -> None:
    assert tariff_for(100) is Tariff.B  # cố ý viết sai


def test_tariff_d_applies_to_300m3(usage: int) -> None:
    assert tariff_for(usage) is Tariff.D  # không có fixture nào tên là usage
