from decimal import Decimal

import pytest

from app.services.tax_service import calculate_gst
from app.utils.currency import format_currency


def test_gst_is_five_percent_and_rounded_to_two_places() -> None:
    assert calculate_gst(Decimal("500.00")) == Decimal("25.00")
    assert calculate_gst(Decimal("1.11")) == Decimal("0.06")


def test_negative_taxable_amount_is_rejected() -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        calculate_gst(Decimal("-1.00"))


@pytest.mark.parametrize(
    ("amount", "formatted"),
    [
        ("99", "₹99.00"),
        ("249.5", "₹249.50"),
        ("1249.5", "₹1,249.50"),
    ],
)
def test_currency_formatting(amount: str, formatted: str) -> None:
    assert format_currency(Decimal(amount)) == formatted
