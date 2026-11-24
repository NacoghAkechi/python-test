"""Tính tiền gas (Entities)."""

from gas.tariff import PRICES, tariff_for


def gas_charge(usage: int) -> int:
    """Từ lượng dùng trong 1 tháng (㎥), trả về tiền gas (yên, đã gồm thuế).

    Tiền gas = phí cơ bản + đơn giá × lượng dùng. Bỏ phần lẻ dưới 1 yên.
    Phí cơ bản và đơn giá lấy theo bảng giá ứng với lượng dùng.
    Số âm thì ValueError("usage must not be negative").
    """
    basic_fee, unit_price = PRICES[tariff_for(usage)]
    return int(basic_fee + unit_price * usage)  # int bỏ phần lẻ dưới 1 yên
