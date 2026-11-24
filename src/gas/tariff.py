"""Quy tắc của bảng giá (Entities). Chỉ có hàm thuần, không biết gì về Django hay DB.

PRICES là giá thông thường (一般料金, 東京地区等) của Tokyo Gas, kỳ 2026年11月検針分 (công bố 2026-09-29, lấy về 2026-11-19).
Đơn giá đổi hằng tháng nên cố định theo tháng này. Ảnh chụp lúc lấy: docs/tokyo-gas-2026-11-tariff.png (docs/README.md)
Nguồn: https://www.tokyo-gas.co.jp/news/press/20260929-02_01.pdf
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


# (phí cơ bản yên/tháng, đơn giá yên/㎥) của từng bảng giá. Đều đã gồm thuế
PRICES = {
    Tariff.A: (Decimal("909.00"), Decimal("190.94")),
    Tariff.B: (Decimal("1206.00"), Decimal("176.09")),
    Tariff.C: (Decimal("1382.00"), Decimal("173.89")),
    Tariff.D: (Decimal("2042.00"), Decimal("170.59")),
    Tariff.E: (Decimal("6442.00"), Decimal("161.79")),
    Tariff.F: (Decimal("12602.00"), Decimal("154.09")),
}


def tariff_for(usage: int) -> Tariff:
    """Từ lượng dùng trong 1 tháng (㎥), xác định bảng giá được áp dụng.

    0〜20㎥ là A, 21〜80㎥ là B, 81〜200㎥ là C,
    201〜500㎥ là D, 501〜800㎥ là E, từ 801㎥ là F.
    Số âm thì ValueError("usage must not be negative").
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
