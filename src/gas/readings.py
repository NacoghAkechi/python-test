"""Tính lượng dùng từ chỉ số đồng hồ gas."""


def usage_between(previous: int, current: int) -> int:
    """Từ chỉ số lần trước và lần này (㎥), trả về lượng dùng ở giữa (㎥).

    - Lượng dùng = chỉ số lần này − chỉ số lần trước
    - Đồng hồ có 4 chữ số, sau 9999㎥ quay về 0㎥. Chỉ số lần này nhỏ hơn lần trước thì coi là đã quay hết một vòng
    - Chỉ số nằm ngoài 0〜9999 thì ValueError("reading must be between 0 and 9999")
    """
    if current <= previous:
        return current + 9999 - previous
    return current - previous
