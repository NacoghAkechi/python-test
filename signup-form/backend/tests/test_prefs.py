"""prefs.json（47 都道府県）のテスト。

都道府県は、conftest.py の django_db_setup が、テストの最初に登録している。
"""

import pytest

from accounts.models import Pref

pytestmark = pytest.mark.django_db


def test_47_prefs_are_registered() -> None:
    # Act
    count = Pref.objects.count()

    # Assert
    assert count == 47


def test_prefs_are_ordered_by_code() -> None:
    # Act
    prefs = list(Pref.objects.order_by("code"))

    # Assert
    assert (prefs[0].code, prefs[0].name) == (1, "北海道")
    assert (prefs[13].code, prefs[13].name) == (13, "東京都")
    assert (prefs[-1].code, prefs[-1].name) == (47, "沖縄県")
