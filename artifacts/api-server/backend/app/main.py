"""FastAPI application factory and server entry point."""

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router
from .repository import OrderRepository


def create_app(database_path: str | Path | None = None) -> FastAPI:
    app = FastAPI(
        title="Rasoi Route Billing API",
        description="Decimal-safe Indian food ordering, discounts, delivery, GST, and invoices.",
        version="1.0.0",
    )
    resolved_path = database_path or os.environ.get(
        "RASOI_DB_PATH",
        str(Path(__file__).resolve().parents[1] / "rasoi_orders.sqlite3"),
    )
    app.state.order_repository = OrderRepository(resolved_path)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app


app = create_app()
