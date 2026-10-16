from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.models.food import OrderInput
from app.services.billing_service import BillingService, UnknownMenuItemError


def test_empty_orders_are_rejected() -> None:
    with pytest.raises(ValidationError):
        OrderInput(items=[])


@pytest.mark.parametrize("quantity", [0, -1, 100])
def test_invalid_quantities_are_rejected(quantity: int) -> None:
    with pytest.raises(ValidationError):
        OrderInput(items=[{"itemId": "idli", "quantity": quantity}])


def test_invalid_menu_id_is_rejected() -> None:
    order = OrderInput(items=[{"itemId": "not-on-menu", "quantity": 1}])
    with pytest.raises(UnknownMenuItemError, match="Unknown menu item"):
        BillingService().calculate(order)


def test_duplicate_line_quantities_cannot_bypass_limit() -> None:
    order = OrderInput(
        items=[
            {"itemId": "idli", "quantity": 60},
            {"itemId": "idli", "quantity": 40},
        ]
    )
    with pytest.raises(ValueError, match="cannot exceed 99"):
        BillingService().calculate(order)


def test_client_cannot_supply_a_price_or_final_total() -> None:
    order = OrderInput.model_validate(
        {
            "items": [{"itemId": "idli", "quantity": 1}],
            "price": "0.01",
            "total": "0.01",
        }
    )
    bill = BillingService().calculate(order)
    assert bill.items[0].unitPrice == Decimal("99.00")
