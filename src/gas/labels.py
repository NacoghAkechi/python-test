"""料金の表示。"""


def format_price(price: int) -> str:
    """料金を「1,000円」の形にする。"""
    return f"{price:,}円"


def parse_price(label: str) -> int:
    """「1,000円」の形の文字列を、料金に戻す。"""
    return int(label.removesuffix("円").replace(",", "", 1))
