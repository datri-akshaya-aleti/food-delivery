from decimal import Decimal

from hypothesis import given, settings
from hypothesis import strategies as st

from app.services.billing_service import BillingService
from app.services.subtotal_service import PricedLine, calculate_subtotal
from app.services.tax_service import calculate_gst
from app.strategies.discount import BestAvailableDiscount
from app.utils.currency import ZERO


@given(
    price_cents=st.integers(min_value=1, max_value=100_000_000),
    first_quantity=st.integers(min_value=1, max_value=99),
    additional_quantity=st.integers(min_value=0, max_value=99),
)
@settings(max_examples=150)
def test_subtotal_is_non_negative_and_increases_with_quantity(
    price_cents: int,
    first_quantity: int,
    additional_quantity: int,
) -> None:
    price = Decimal(price_cents) / Decimal("100")
    first = calculate_subtotal([PricedLine("item", "Property item", first_quantity, price)])
    increased = calculate_subtotal(
        [PricedLine("item", "Property item", first_quantity + additional_quantity, price)]
    )
    assert first >= Decimal("0.00")
    assert increased >= first


@given(subtotal_cents=st.integers(min_value=0, max_value=1_000_000_000))
@settings(max_examples=150)
def test_subtotal_never_becomes_negative(subtotal_cents: int) -> None:
    subtotal = Decimal(subtotal_cents) / Decimal("100")
    lines = [PricedLine("item", "Property item", 1, subtotal)]
    assert calculate_subtotal(lines) >= Decimal("0.00")


@given(subtotal_cents=st.integers(min_value=0, max_value=1_000_000_000))
@settings(max_examples=150)
def test_discount_is_never_negative_and_never_exceeds_subtotal(subtotal_cents: int) -> None:
    subtotal = Decimal(subtotal_cents) / Decimal("100")
    for coupon in (None, "WELCOME50", "SAVE10", "FESTIVE20"):
        amount, _label = BestAvailableDiscount().calculate(subtotal, coupon)
        assert amount >= ZERO
        assert amount <= subtotal


@given(taxable_cents=st.integers(min_value=0, max_value=1_000_000_000))
@settings(max_examples=150)
def test_gst_is_never_negative(taxable_cents: int) -> None:
    taxable = Decimal(taxable_cents) / Decimal("100")
    assert calculate_gst(taxable) >= ZERO


@given(
    quantity=st.integers(min_value=1, max_value=40),
    extra=st.integers(min_value=1, max_value=5),
)
@settings(max_examples=80)
def test_final_bill_is_never_negative_and_quantity_cannot_reduce_subtotal(
    quantity: int,
    extra: int,
) -> None:
    service = BillingService()
    smaller = service.calculate_priced_lines(
        [PricedLine("demo", "Demo", quantity, Decimal("99.00"))]
    )
    larger = service.calculate_priced_lines(
        [PricedLine("demo", "Demo", quantity + extra, Decimal("99.00"))]
    )
    assert smaller.subtotal >= ZERO
    assert smaller.discount >= ZERO
    assert smaller.gst >= ZERO
    assert smaller.total >= ZERO
    assert larger.subtotal >= smaller.subtotal
    assert larger.total >= ZERO
