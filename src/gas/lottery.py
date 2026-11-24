"""検針のお楽しみ抽選。"""

import random


def lucky_charge(charge: int) -> int:
    """抽選に当たったら、今月のガス料金を半額にする。当たる確率は 2 分の 1。"""
    if random.random() < 0.5:
        return charge // 2
    return charge
