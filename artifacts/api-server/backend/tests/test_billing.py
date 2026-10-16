from decimal import Decimal

from app.menu import MENU_BY_ID
from app.models.food import OrderInput
from app.services.billing_service import BillingService
from app.services.subtotal_service import PricedLine
from app.strategies.discount import FlatDiscount


def test_single_item_uses_rupees_and_includes_delivery_in_gst_base() -> None:
    bill = BillingService().calculate(OrderInput(items=[{"itemId": "samosa", "quantity": 1}]))
    assert bill.subtotal == Decimal("49.00")
    assert bill.discount == Decimal("0.00")
    assert bill.delivery == Decimal("40.00")
    assert bill.gst == Decimal("4.45")
    assert bill.total == Decimal("93.45")


def test_multiple_items_and_duplicate_items_are_combined() -> None:
    bill = BillingService().calculate(
        OrderInput(
            items=[
                {"itemId": "idli", "quantity": 2},
                {"itemId": "butter-naan", "quantity": 1},
                {"itemId": "idli", "quantity": 1},
            ]
        )
    )
    assert bill.subtotal == Decimal("356.00")
    assert [(line.itemId, line.quantity) for line in bill.items] == [
        ("idli", 3),
        ("butter-naan", 1),
    ]
    assert bill.discount == Decimal("0.00")
    assert bill.delivery == Decimal("30.00")
    assert bill.gst == Decimal("19.30")
    assert bill.total == Decimal("405.30")


def test_requested_defence_demo_order() -> None:
    bill = BillingService().calculate(
        OrderInput(
            items=[
                {"itemId": "chicken-biryani", "quantity": 2},
                {"itemId": "chicken-65", "quantity": 1},
                {"itemId": "butter-naan", "quantity": 2},
                {"itemId": "mango-lassi", "quantity": 1},
            ]
        )
    )
    assert bill.subtotal == Decimal("914.00")
    assert bill.discount == Decimal("91.40")
    assert bill.delivery == Decimal("20.00")
    assert bill.gst == Decimal("42.13")
    assert bill.total == Decimal("884.73")


def test_reference_example_taxes_discounted_food_plus_delivery() -> None:
    bill = BillingService().calculate(
        OrderInput(
            items=[
                {"itemId": "masala-dosa", "quantity": 1},
                {"itemId": "idli", "quantity": 1},
                {"itemId": "butter-naan", "quantity": 6},
                {"itemId": "samosa", "quantity": 2},
            ]
        )
    )
    assert bill.subtotal == Decimal("700.00")
    assert bill.discount == Decimal("70.00")
    assert bill.delivery == Decimal("20.00")
    assert bill.gst == Decimal("32.50")
    assert bill.total == Decimal("682.50")


def test_all_authoritative_menu_prices_are_rupees() -> None:
    assert len(MENU_BY_ID) == 16
    assert all(item.price > Decimal("0.00") for item in MENU_BY_ID.values())
    assert all(isinstance(item.price, Decimal) for item in MENU_BY_ID.values())
    assert "gulab-jamun" not in MENU_BY_ID


def test_discount_is_capped_at_subtotal() -> None:
    service = BillingService(
        discount_strategy=FlatDiscount(Decimal("100.00"), "Oversized discount")
    )
    bill = service.calculate(OrderInput(items=[{"itemId": "samosa", "quantity": 1}]))
    assert bill.discount == bill.subtotal == Decimal("49.00")
    assert bill.total >= Decimal("0.00")


def test_large_order_stays_linear_and_non_negative() -> None:
    bill = BillingService().calculate_priced_lines(
        [PricedLine("line", "Large order dish", 1, Decimal("99.00")) for _ in range(200)]
    )
    assert bill.subtotal == Decimal("19800.00")
    assert bill.discount == Decimal("3960.00")
    assert bill.delivery == Decimal("0.00")
    assert bill.gst == Decimal("792.00")
    assert bill.total == Decimal("16632.00")
    assert bill.total >= Decimal("0.00")


def test_percent_coupon_competes_with_tier_discount() -> None:
    bill = BillingService().calculate(
        OrderInput(items=[{"itemId": "idli", "quantity": 6}], coupon="FESTIVE20")
    )
    assert bill.subtotal == Decimal("594.00")
    assert bill.discount == Decimal("118.80")
    assert bill.discountLabel == "FESTIVE20 coupon"
