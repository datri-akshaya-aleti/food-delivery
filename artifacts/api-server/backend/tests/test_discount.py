from decimal import Decimal

import pytest

from app.strategies.discount import (
    BestAvailableDiscount,
    FestivalDiscount,
    FlatDiscount,
    InvalidCouponError,
    NoDiscount,
    PercentageDiscount,
    TieredDiscount,
)


@pytest.mark.parametrize(
    ("subtotal", "expected", "label"),
    [
        ("499.99", "0.00", "No discount"),
        ("500.00", "50.00", "10% order discount"),
        ("999.99", "100.00", "10% order discount"),
        ("1000.00", "150.00", "15% order discount"),
        ("1499.99", "225.00", "15% order discount"),
        ("1500.00", "300.00", "20% order discount"),
    ],
)
def test_tiered_discount_boundaries(subtotal: str, expected: str, label: str) -> None:
    amount, actual_label = TieredDiscount().calculate(Decimal(subtotal))
    assert amount == Decimal(expected)
    assert actual_label == label


def test_concrete_strategy_types() -> None:
    assert NoDiscount().calculate(Decimal("100.00"))[0] == Decimal("0.00")
    assert PercentageDiscount(Decimal("0.10"), "SAVE10").calculate(Decimal("250.00"))[0] == Decimal(
        "25.00"
    )
    assert FlatDiscount(Decimal("50.00"), "WELCOME50").calculate(Decimal("100.00"))[0] == Decimal(
        "50.00"
    )
    assert FestivalDiscount().calculate(Decimal("500.00"))[0] == Decimal("100.00")


@pytest.mark.parametrize(
    ("coupon", "subtotal", "expected"),
    [
        ("WELCOME50", "249.00", "50.00"),
        ("SAVE10", "249.00", "24.90"),
        ("FESTIVE20", "249.00", "49.80"),
    ],
)
def test_supported_coupons(coupon: str, subtotal: str, expected: str) -> None:
    amount, _label = BestAvailableDiscount().calculate(Decimal(subtotal), coupon)
    assert amount == Decimal(expected)


def test_invalid_coupon_is_rejected() -> None:
    with pytest.raises(InvalidCouponError, match="Invalid coupon"):
        BestAvailableDiscount().calculate(Decimal("500.00"), "NOT-A-COUPON")
