"""Composable delivery-fee strategies."""

from abc import ABC, abstractmethod
from decimal import Decimal

from ..utils.currency import ZERO


class DeliveryStrategy(ABC):
    @abstractmethod
    def calculate(self, subtotal: Decimal) -> tuple[Decimal, str]:
        """Return a delivery charge and its display label."""


class StandardDelivery(DeliveryStrategy):
    """Apply the requested subtotal-based delivery bands."""

    def calculate(self, subtotal: Decimal) -> tuple[Decimal, str]:
        if subtotal >= Decimal("1000.00"):
            return ZERO, "Free delivery"
        if subtotal >= Decimal("600.00"):
            return Decimal("20.00"), "Standard delivery"
        if subtotal >= Decimal("300.00"):
            return Decimal("30.00"), "Standard delivery"
        return Decimal("40.00"), "Standard delivery"


class FreeDelivery(DeliveryStrategy):
    def calculate(self, subtotal: Decimal) -> tuple[Decimal, str]:
        del subtotal
        return ZERO, "Free delivery"


class DistanceBasedDelivery(DeliveryStrategy):
    """An optional strategy for a future real delivery-distance provider."""

    def __init__(
        self,
        distance_km: Decimal,
        base_charge: Decimal = Decimal("20.00"),
        per_km_charge: Decimal = Decimal("5.00"),
        max_distance_km: Decimal = Decimal("20.00"),
    ) -> None:
        if distance_km < 0 or distance_km > max_distance_km:
            raise ValueError("Delivery distance is outside the service area")
        self.distance_km = distance_km
        self.base_charge = base_charge
        self.per_km_charge = per_km_charge

    def calculate(self, subtotal: Decimal) -> tuple[Decimal, str]:
        del subtotal
        charge = self.base_charge + self.distance_km * self.per_km_charge
        return charge.quantize(Decimal("0.01")), f"Distance delivery · {self.distance_km} km"
