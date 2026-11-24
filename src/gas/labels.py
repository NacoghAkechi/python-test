"""Hiển thị số tiền."""


def format_price(price: int) -> str:
    """Đổi số tiền sang dạng 「1,000円」."""
    return f"{price:,}円"


def parse_price(label: str) -> int:
    """Đổi chuỗi dạng 「1,000円」 về số tiền."""
    return int(label.removesuffix("円").replace(",", "", 1))
