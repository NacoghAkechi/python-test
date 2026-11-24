"""Quy tắc của chương trình khuyến mãi tiết kiệm cuối năm."""

from datetime import date

CAMPAIGN_DISCOUNT = 1000
GIFT_USAGE_LIMIT = 20


def is_campaign_period(day: date) -> bool:
    """Ngày ghi chỉ số từ 1/12 đến 25/12 thì thuộc thời gian khuyến mãi."""
    return date(day.year, 12, 1) <= day <= date(day.year, 12, 25)


def campaign_charge(charge: int, read_on: date) -> int:
    """Trong thời gian khuyến mãi thì giảm 1,000 yên tiền gas. Không xuống dưới 0 yên."""
    if is_campaign_period(read_on):
        return max(charge - CAMPAIGN_DISCOUNT, 0)
    return charge


def gets_gift(web_statement: bool, usage: int) -> bool:
    """Người dùng Web 明細 chỉ dùng tối đa 20㎥ thì được tặng quà."""
    return web_statement and usage <= GIFT_USAGE_LIMIT
