"""Decimal-safe INR rounding and display formatting."""

from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")
ZERO = Decimal("0.00")


def quantize_money(value: Decimal) -> Decimal:
    """Round a rupee amount to two decimal places using half-up rounding."""

    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def format_currency(value: Decimal) -> str:
    """Format a rupee amount with Indian digit grouping and two decimal places."""

    return f"₹{quantize_money(value):,.2f}"
