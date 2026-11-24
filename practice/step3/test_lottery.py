from gas.lottery import lucky_charge


def test_winner_pays_half() -> None:
    assert lucky_charge(6488) == 3244
