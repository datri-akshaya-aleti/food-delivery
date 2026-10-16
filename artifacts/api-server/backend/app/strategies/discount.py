"""Composable tier and coupon discount strategies."""

from abc import ABC, abstractmethod
from decimal import Decimal

from ..menu import VALID_COUPONS
from ..utils.currency import ZERO, quantize_money

DiscountQuote = tuple[Decimal, str]


class InvalidCouponError(ValueError):
    """Raised when a submitted coupon is not supported."""


class DiscountStrategy(ABC):
    """Abstraction used by BillingService to calculate discounts."""

    @abstractmethod
    def calculate(self, subtotal: Decimal, coupon_code: str | None = None) -> DiscountQuote:
        """Return a non-negative discount amount and its display label."""


class NoDiscount(DiscountStrategy):
    def calculate(self, subtotal: Decimal, coupon_code: str | None = None) -> DiscountQuote:
        del subtotal, coupon_code
        return ZERO, "No discount"


class PercentageDiscount(DiscountStrategy):
    def __init__(self, rate: Decimal, label: str) -> None:
        if rate < 0 or rate > 1:
            raise ValueError("Discount rate must be between zero and one")
        self.rate = rate
        self.label = label

    def calculate(self, subtotal: Decimal, coupon_code: str | None = None) -> DiscountQuote:
        del coupon_code
        return quantize_money(subtotal * self.rate), self.label


class FlatDiscount(DiscountStrategy):
    def __init__(self, amount: Decimal, label: str) -> None:
        if amount < 0:
            raise ValueError("Flat discount cannot be negative")
        self.amount = amount
        self.label = label

    def calculate(self, subtotal: Decimal, coupon_code: str | None = None) -> DiscountQuote:
        del subtotal, coupon_code
        return self.amount, self.label


class FestivalDiscount(PercentageDiscount):
    def __init__(self) -> None:
        super().__init__(Decimal("0.20"), "FESTIVE20 coupon")


class TieredDiscount(DiscountStrategy):
    """Apply the best subtotal tier: 0%, 10%, 15%, or 20%."""

    def calculate(self, subtotal: Decimal, coupon_code: str | None = None) -> DiscountQuote:
        del coupon_code
        if subtotal >= Decimal("1500.00"):
            return PercentageDiscount(Decimal("0.20"), "20% order discount").calculate(subtotal)
        if subtotal >= Decimal("1000.00"):
            return PercentageDiscount(Decimal("0.15"), "15% order discount").calculate(subtotal)
        if subtotal >= Decimal("500.00"):
            return PercentageDiscount(Decimal("0.10"), "10% order discount").calculate(subtotal)
        return NoDiscount().calculate(subtotal)


class BestAvailableDiscount(DiscountStrategy):
    """Compare an eligible coupon with the tier discount; never stack both."""

    def __init__(self) -> None:
        self.tiered = TieredDiscount()
        self.coupons: dict[str, DiscountStrategy] = {
            "WELCOME50": FlatDiscount(Decimal("50.00"), "WELCOME50 coupon"),
            "SAVE10": PercentageDiscount(Decimal("0.10"), "SAVE10 coupon"),
            "FESTIVE20": FestivalDiscount(),
        }

    def calculate(self, subtotal: Decimal, coupon_code: str | None = None) -> DiscountQuote:
        tier_amount, tier_label = self.tiered.calculate(subtotal)
        if coupon_code is None:
            return min(tier_amount, subtotal), tier_label

        normalized = coupon_code.strip().upper()
        if normalized not in VALID_COUPONS:
            raise InvalidCouponError("Invalid coupon code. Try WELCOME50, SAVE10 or FESTIVE20.")

        coupon_amount, coupon_label = self.coupons[normalized].calculate(subtotal)
        amount, label = (
            (coupon_amount, coupon_label)
            if coupon_amount > tier_amount
            else (tier_amount, tier_label)
        )
        return min(max(amount, ZERO), subtotal), label
