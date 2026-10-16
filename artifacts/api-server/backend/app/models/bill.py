"""Authoritative invoice response models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .food import Money


class BillLine(BaseModel):
    model_config = ConfigDict(frozen=True)

    itemId: str
    name: str
    quantity: int
    unitPrice: Money
    total: Money


class Bill(BaseModel):
    model_config = ConfigDict(frozen=True)

    orderId: str
    createdAt: datetime
    items: list[BillLine]
    subtotal: Money
    discount: Money
    discountLabel: str
    delivery: Money
    deliveryLabel: str
    gst: Money
    total: Money
    coupon: str | None
