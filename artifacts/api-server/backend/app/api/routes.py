"""REST endpoints for menu, orders, and educational demonstrations."""

import asyncio
import statistics
import time
from datetime import datetime
from decimal import Decimal
from typing import Annotated, cast

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel

from ..menu import MENU
from ..models.bill import Bill
from ..models.food import CouponInput, FoodItem, OrderInput
from ..repository import OrderRepository
from ..services.billing_service import BillingService
from ..services.io_bound import (
    check_serviceability,
    estimate_delivery_minutes,
    lookup_coupon,
)
from ..services.subtotal_service import PricedLine

router = APIRouter(prefix="/api")


class DeliveryAvailability(BaseModel):
    postalCode: str
    available: bool
    estimatedMinutes: int
    checksCompleted: int
    detail: str


class BenchmarkMeasurement(BaseModel):
    itemCount: int
    elapsedMilliseconds: float


class BenchmarkResult(BaseModel):
    measurements: list[BenchmarkMeasurement]
    complexity: str
    note: str


def get_repository(request: Request) -> OrderRepository:
    return cast(OrderRepository, request.app.state.order_repository)


RepositoryDependency = Annotated[OrderRepository, Depends(get_repository)]


@router.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/menu", response_model=list[FoodItem])
async def get_menu() -> list[FoodItem]:
    return list(MENU)


@router.post("/orders/calculate", response_model=Bill)
async def calculate_order(order: OrderInput) -> Bill:
    try:
        return BillingService().calculate(order)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(error),
        ) from error


@router.post("/orders", response_model=Bill, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderInput, repository: RepositoryDependency) -> Bill:
    try:
        bill = BillingService().calculate(order)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(error),
        ) from error
    repository.save(bill.orderId, bill.createdAt.isoformat(), order)
    return bill


@router.post("/orders/{order_id}/bill", response_model=Bill)
async def get_order_bill(order_id: str, repository: RepositoryDependency) -> Bill:
    saved = repository.get(order_id)
    if saved is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    created_at = datetime.fromisoformat(saved.created_at)
    try:
        return BillingService().calculate(
            saved.request,
            order_id=saved.order_id,
            created_at=created_at,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(error),
        ) from error


@router.post("/orders/{order_id}/coupon", response_model=Bill)
async def apply_order_coupon(
    order_id: str,
    coupon_input: CouponInput,
    repository: RepositoryDependency,
) -> Bill:
    saved = repository.get(order_id)
    if saved is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    catalog_code = await lookup_coupon(coupon_input.coupon)
    if catalog_code is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid coupon code. Try WELCOME50, SAVE10 or FESTIVE20.",
        )
    updated_request = saved.request.model_copy(update={"coupon": catalog_code})
    try:
        bill = BillingService().calculate(
            updated_request,
            order_id=saved.order_id,
            created_at=datetime.fromisoformat(saved.created_at),
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(error),
        ) from error
    repository.update(order_id, updated_request)
    return bill


@router.get("/delivery/availability", response_model=DeliveryAvailability)
async def check_delivery_availability(
    postal_code: Annotated[
        str,
        Query(alias="postalCode", min_length=6, max_length=6, pattern=r"^\d{6}$"),
    ],
) -> DeliveryAvailability:
    available, estimated_minutes = await asyncio.gather(
        check_serviceability(postal_code),
        estimate_delivery_minutes(postal_code),
    )
    return DeliveryAvailability(
        postalCode=postal_code,
        available=available,
        estimatedMinutes=estimated_minutes,
        checksCompleted=2,
        detail="Demo provider calls are simulated for the concurrency lesson.",
    )


@router.get("/performance/benchmark", response_model=BenchmarkResult)
async def run_billing_benchmark() -> BenchmarkResult:
    service = BillingService()
    measurements: list[BenchmarkMeasurement] = []
    for item_count in (10, 100, 1_000, 10_000):
        lines = [
            PricedLine(
                item_id=f"benchmark-{index}",
                name="Benchmark dish",
                quantity=1,
                unit_price=Decimal("99.00"),
            )
            for index in range(item_count)
        ]
        samples: list[float] = []
        for _ in range(5):
            started = time.perf_counter_ns()
            service.calculate_priced_lines(lines)
            samples.append((time.perf_counter_ns() - started) / 1_000_000)
        measurements.append(
            BenchmarkMeasurement(
                itemCount=item_count,
                elapsedMilliseconds=round(statistics.median(samples), 4),
            )
        )
    return BenchmarkResult(
        measurements=measurements,
        complexity="O(n) time and O(n) space",
        note="Measured live on this server; each point is the median of five local runs.",
    )
