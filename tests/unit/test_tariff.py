from gas.tariff import Tariff, tariff_for


def test_10m3_uses_tariff_a() -> None:
    # Arrange
    usage = 10

    # Act
    tariff = tariff_for(usage)

    # Assert
    assert tariff is Tariff.A


def test_30m3_uses_tariff_b() -> None:
    # Arrange
    usage = 30

    # Act
    tariff = tariff_for(usage)

    # Assert
    assert tariff is Tariff.B
