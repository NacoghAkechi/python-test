from gas.labels import format_price, parse_price


def test_format_price_adds_comma_and_yen() -> None:
    assert format_price(6488) == "6,488円"


def test_parse_price_reads_label_with_comma() -> None:
    assert parse_price("6,488円") == 6488


def test_parse_price_reads_label_without_comma() -> None:
    assert parse_price("909円") == 909
