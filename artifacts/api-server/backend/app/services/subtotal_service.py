"""Pure subtotal calculations."""

from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal

from ..utils.currency import ZERO, quantize_money


@dataclass(frozen=True, slots=True)
class PricedLine:
    """A trusted menu line resolved by the backend."""

    item_id: str
    name: str
    quantity: int
    unit_price: Decimal

    @property
    def total(self) -> Decimal:
        return calculate_item_total(self.unit_price, self.quantity)


def calculate_item_total(price: Decimal, quantity: int) -> Decimal:
    """Purely calculate one line total."""

    return quantize_money(price * quantity)


def calculate_subtotal(lines: Iterable[PricedLine]) -> Decimal:
    """Sum line totals in O(n) time, using Decimal arithmetic."""

    return quantize_money(sum((line.total for line in lines), start=ZERO))
