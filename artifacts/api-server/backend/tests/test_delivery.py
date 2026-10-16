from decimal import Decimal

import pytest

from app.strategies.delivery import DistanceBasedDelivery, FreeDelivery, StandardDelivery


@pytest.mark.parametrize(
    ("subtotal", "expected"),
    [
        ("0.00", "40.00"),
        ("299.99", "40.00"),
        ("300.00", "30.00"),
        ("599.99", "30.00"),
        ("600.00", "20.00"),
        ("999.99", "20.00"),
        ("1000.00", "0.00"),
    ],
)
def test_delivery_thresholds(subtotal: str, expected: str) -> None:
    charge, _label = StandardDelivery().calculate(Decimal(subtotal))
    assert charge == Decimal(expected)


def test_free_delivery_strategy() -> None:
    assert FreeDelivery().calculate(Decimal("80.00")) == (
        Decimal("0.00"),
        "Free delivery",
    )


def test_distance_strategy_and_service_area_validation() -> None:
    charge, label = DistanceBasedDelivery(Decimal("2.00")).calculate(Decimal("50.00"))
    assert charge == Decimal("30.00")
    assert "2.00 km" in label
    with pytest.raises(ValueError, match="service area"):
        DistanceBasedDelivery(Decimal("21.00"))
