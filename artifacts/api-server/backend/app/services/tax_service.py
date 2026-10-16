"""GST calculation."""

from decimal import Decimal

from ..utils.currency import quantize_money

GST_RATE = Decimal("0.05")


def calculate_gst(taxable_amount: Decimal) -> Decimal:
    """Calculate 5% GST on the post-discount amount, including delivery."""

    if taxable_amount < 0:
        raise ValueError("Taxable amount cannot be negative")
    return quantize_money(taxable_amount * GST_RATE)
