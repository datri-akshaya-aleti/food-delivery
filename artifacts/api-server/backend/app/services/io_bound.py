"""Educational helpers for I/O-bound work.

Billing arithmetic is CPU-bound but tiny: a linear Decimal pass. It stays
sequential because spinning extra processes would cost more than it saves.

Delivery coverage and coupon catalogs are I/O-bound. Those waits belong in
asyncio so the event loop can service other requests. The GIL does not matter
here: the thread is idle during `await`, not computing in parallel.
"""

import asyncio

from ..menu import VALID_COUPONS


async def check_serviceability(postal_code: str) -> bool:
    """Simulate an I/O-bound carrier/serviceability lookup."""

    await asyncio.sleep(0.015)
    return postal_code.startswith(("5", "6"))


async def estimate_delivery_minutes(postal_code: str) -> int:
    """Simulate a second independent I/O-bound estimate call."""

    await asyncio.sleep(0.015)
    return 35 if postal_code.startswith("5") else 45


async def lookup_coupon(code: str) -> str | None:
    """Simulate an I/O-bound coupon catalog lookup."""

    await asyncio.sleep(0.01)
    normalized = code.strip().upper()
    return normalized if normalized in VALID_COUPONS else None
