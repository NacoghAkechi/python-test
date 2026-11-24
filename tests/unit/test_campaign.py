from datetime import date

import pytest

from gas.campaign import campaign_charge, gets_gift, is_campaign_period


@pytest.mark.parametrize(
    ("day", "expected"),
    [
        pytest.param(date(2026, 11, 30), False, id="day_before_campaign"),
        pytest.param(date(2026, 12, 1), True, id="first_day"),
        pytest.param(date(2026, 12, 10), True, id="middle_of_campaign"),
        pytest.param(date(2026, 12, 26), False, id="day_after_campaign"),
    ],
)
def test_campaign_runs_from_december_1_to_25(day: date, expected: bool) -> None:
    assert is_campaign_period(day) is expected


def test_campaign_takes_1000_yen_off_during_campaign() -> None:
    assert campaign_charge(6488, date(2026, 12, 10)) == 5488


def test_charge_is_unchanged_outside_campaign() -> None:
    assert campaign_charge(6488, date(2026, 11, 30)) == 6488


def test_campaign_charge_never_goes_below_zero() -> None:
    assert campaign_charge(909, date(2026, 12, 10)) >= 0


@pytest.mark.parametrize(
    ("web_statement", "usage", "expected"),
    [
        pytest.param(True, 20, True, id="web_statement_exactly_20m3"),
        pytest.param(False, 30, False, id="paper_statement_30m3"),
    ],
)
def test_gift_goes_to_web_statement_users_who_use_20m3_or_less(
    web_statement: bool, usage: int, expected: bool
) -> None:
    assert gets_gift(web_statement, usage) is expected
