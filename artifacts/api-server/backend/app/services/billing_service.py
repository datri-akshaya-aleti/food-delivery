"""Authoritative order-to-invoice calculation service."""

from datetime import UTC, datetime
from uuid import uuid4

from ..menu import MENU_BY_ID
from ..models.bill import Bill, BillLine
from ..models.food import OrderInput
from ..strategies.delivery import DeliveryStrategy, StandardDelivery
from ..strategies.discount import BestAvailableDiscount, DiscountStrategy
from ..utils.currency import ZERO, quantize_money
from .subtotal_service import PricedLine, calculate_subtotal
from .tax_service import calculate_gst


class UnknownMenuItemError(ValueError):
    """Raised when an order references an ID that is not in the menu."""


class BillingService:
    def __init__(
        self,
        discount_strategy: DiscountStrategy | None = None,
        delivery_strategy: DeliveryStrategy | None = None,
    ) -> None:
        self.discount_strategy = discount_strategy or BestAvailableDiscount()
        self.delivery_strategy = delivery_strategy or StandardDelivery()

    def calculate(
        self,
        order: OrderInput,
        *,
        order_id: str | None = None,
        created_at: datetime | None = None,
    ) -> Bill:
        """Resolve trusted menu prices, merge duplicates, and calculate all bill lines."""

        quantities: dict[str, int] = {}
        for item in order.items:
            quantities[item.itemId] = quantities.get(item.itemId, 0) + item.quantity
            if quantities[item.itemId] > 99:
                raise ValueError(f"Quantity for {item.itemId} cannot exceed 99")

        priced_lines: list[PricedLine] = []
        for item_id, quantity in quantities.items():
            food = MENU_BY_ID.get(item_id)
            if food is None:
                raise UnknownMenuItemError(f"Unknown menu item: {item_id}")
            priced_lines.append(
                PricedLine(
                    item_id=item_id,
                    name=food.name,
                    quantity=quantity,
                    unit_price=food.price,
                )
            )
        return self.calculate_priced_lines(
            priced_lines,
            coupon=order.coupon,
            order_id=order_id,
            created_at=created_at,
        )

    def calculate_priced_lines(
        self,
        lines: list[PricedLine],
        *,
        coupon: str | None = None,
        order_id: str | None = None,
        created_at: datetime | None = None,
    ) -> Bill:
        """Calculate the shared production and benchmark billing path."""

        if not lines:
            raise ValueError("An order must contain at least one item")
        subtotal = calculate_subtotal(lines)
        discount, discount_label = self.discount_strategy.calculate(subtotal, coupon)
        discount = min(max(quantize_money(discount), ZERO), subtotal)
        delivery, delivery_label = self.delivery_strategy.calculate(subtotal)
        delivery = quantize_money(delivery)
        taxable_amount = max(ZERO, subtotal - discount) + delivery
        gst = calculate_gst(taxable_amount)
        total = quantize_money(subtotal - discount + delivery + gst)
        return Bill(
            orderId=order_id or f"ORD-{uuid4().hex[:10].upper()}",
            createdAt=created_at or datetime.now(UTC),
            items=[
                BillLine(
                    itemId=line.item_id,
                    name=line.name,
                    quantity=line.quantity,
                    unitPrice=line.unit_price,
                    total=line.total,
                )
                for line in lines
            ],
            subtotal=subtotal,
            discount=discount,
            discountLabel=discount_label,
            delivery=delivery,
            deliveryLabel=delivery_label,
            gst=gst,
            total=total,
            coupon=coupon,
        )
