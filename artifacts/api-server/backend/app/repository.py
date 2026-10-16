"""Small SQLite repository for saved demo orders."""

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from .models.food import OrderInput


@dataclass(frozen=True, slots=True)
class SavedOrder:
    order_id: str
    created_at: str
    request: OrderInput


class OrderRepository:
    def __init__(self, database_path: str | Path) -> None:
        self.database_path = str(database_path)
        Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    request_json TEXT NOT NULL
                )
                """)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path, timeout=10)
        connection.row_factory = sqlite3.Row
        return connection

    def save(self, order_id: str, created_at: str, request: OrderInput) -> None:
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO orders (order_id, created_at, request_json) VALUES (?, ?, ?)",
                (order_id, created_at, request.model_dump_json()),
            )

    def get(self, order_id: str) -> SavedOrder | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT order_id, created_at, request_json FROM orders WHERE order_id = ?",
                (order_id,),
            ).fetchone()
        if row is None:
            return None
        request_data = json.loads(str(row["request_json"]))
        return SavedOrder(
            order_id=str(row["order_id"]),
            created_at=str(row["created_at"]),
            request=OrderInput.model_validate(request_data),
        )

    def update(self, order_id: str, request: OrderInput) -> bool:
        with self._connect() as connection:
            cursor = connection.execute(
                "UPDATE orders SET request_json = ? WHERE order_id = ?",
                (request.model_dump_json(), order_id),
            )
        return cursor.rowcount > 0
