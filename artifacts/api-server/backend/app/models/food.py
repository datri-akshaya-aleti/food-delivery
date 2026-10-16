"""Validated menu and order models."""

from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer, field_validator

Money = Annotated[
    Decimal,
    PlainSerializer(float, return_type=float, when_used="json"),
]

Category = Literal[
    "Biryani",
    "Starters",
    "South Indian",
    "North Indian",
    "Chinese",
    "Desserts",
    "Beverages",
]


class FoodItem(BaseModel):
    """A menu entry whose price is owned by the backend."""

    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    category: Category
    price: Money = Field(gt=0)
    description: str
    imageUrl: str


class OrderItemInput(BaseModel):
    """One requested menu item and its positive quantity."""

    itemId: str = Field(min_length=1, max_length=80)
    quantity: int = Field(ge=1, le=99)


class OrderItem(OrderItemInput):
    """Defence-facing name for a requested order line (IDs and quantity only)."""


class OrderInput(BaseModel):
    """Client input contains IDs and quantities, never trusted prices or totals."""

    items: list[OrderItemInput] = Field(min_length=1, max_length=500)
    coupon: str | None = Field(default=None, max_length=20)

    @field_validator("coupon", mode="before")
    @classmethod
    def normalize_coupon(cls, value: object) -> object:
        if isinstance(value, str):
            normalized = value.strip().upper()
            return normalized or None
        return value


class CouponInput(BaseModel):
    coupon: str = Field(min_length=1, max_length=20)

    @field_validator("coupon")
    @classmethod
    def normalize_coupon(cls, value: str) -> str:
        return value.strip().upper()


class Order(OrderInput):
    """Defence-facing name for a validated order request."""
