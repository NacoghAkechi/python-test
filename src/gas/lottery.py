"""Bốc thăm khi ghi chỉ số."""

import random


def lucky_charge(charge: int) -> int:
    """Nếu trúng thì giảm nửa tiền gas tháng này. Xác suất trúng là 1/2."""
    if random.random() < 0.5:
        return charge // 2
    return charge
