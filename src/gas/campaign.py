"""年末のエコキャンペーンのルール。"""

from datetime import date

CAMPAIGN_DISCOUNT = 1000
GIFT_USAGE_LIMIT = 20


def is_campaign_period(day: date) -> bool:
    """検針日が 12 月 1 日〜25 日なら、キャンペーン期間とする。"""
    return date(day.year, 12, 1) <= day <= date(day.year, 12, 25)


def campaign_charge(charge: int, read_on: date) -> int:
    """キャンペーン期間なら、ガス料金から 1,000 円引く。0 円は下回らない。"""
    if is_campaign_period(read_on):
        return max(charge - CAMPAIGN_DISCOUNT, 0)
    return charge


def gets_gift(web_statement: bool, usage: int) -> bool:
    """Web 明細の人が、使用量を 20㎥ 以下に抑えたら、プレゼントを付ける。"""
    return web_statement and usage <= GIFT_USAGE_LIMIT
