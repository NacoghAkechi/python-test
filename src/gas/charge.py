"""ガス料金の計算（Entities）。"""

from gas.tariff import PRICES, tariff_for


def gas_charge(usage: int) -> int:
    """1 か月の使用量（㎥）から、ガス料金（円・税込）を返す。

    ガス料金 = 基本料金 + 単位料金 × 使用量。1 円未満は切り捨てる。
    基本料金と単位料金は、使用量に応じた料金表のものを使う。
    マイナスなら ValueError("usage must not be negative")。
    """
    basic_fee, unit_price = PRICES[tariff_for(usage)]
    return int(basic_fee + unit_price * usage)  # int は 1 円未満を切り捨てる
