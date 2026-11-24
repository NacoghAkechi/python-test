"""料金表のルール（Entities）。Django も DB も知らない、純粋関数だけを置く。

PRICES は東京ガスの一般料金（東京地区等）の 2026 年 11 月検針分（2026-09-29 発表、2026-11-19 取得）。
単位料金は毎月変わるので、この月の値に固定している。取得時の画面: docs/tokyo-gas-2026-11-tariff.png（docs/README.md）
出典: https://www.tokyo-gas.co.jp/news/press/20260929-02_01.pdf
"""

from decimal import Decimal
from enum import Enum


class Tariff(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"


# 料金表ごとの（基本料金 円/月, 単位料金 円/㎥）。どちらも税込
PRICES = {
    Tariff.A: (Decimal("909.00"), Decimal("190.94")),
    Tariff.B: (Decimal("1206.00"), Decimal("176.09")),
    Tariff.C: (Decimal("1382.00"), Decimal("173.89")),
    Tariff.D: (Decimal("2042.00"), Decimal("170.59")),
    Tariff.E: (Decimal("6442.00"), Decimal("161.79")),
    Tariff.F: (Decimal("12602.00"), Decimal("154.09")),
}


def tariff_for(usage: int) -> Tariff:
    """1 か月の使用量（㎥）から、適用する料金表を決める。

    0〜20㎥ は A、21〜80㎥ は B、81〜200㎥ は C、
    201〜500㎥ は D、501〜800㎥ は E、801㎥ 以上は F。
    マイナスなら ValueError("usage must not be negative")。
    """
    if usage < 0:
        raise ValueError("usage must not be negative")
    if usage <= 20:
        return Tariff.A
    if usage < 80:
        return Tariff.B
    if usage <= 200:
        return Tariff.C
    if usage <= 500:
        return Tariff.D
    if usage <= 800:
        return Tariff.E
    return Tariff.F
