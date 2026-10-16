from fastapi.testclient import TestClient

from app.main import create_app


def test_health_menu_and_calculate_endpoints(tmp_path) -> None:
    client = TestClient(create_app(tmp_path / "orders.sqlite3"))
    assert client.get("/api/health").json() == {"status": "ok"}
    assert client.get("/api/healthz").json() == {"status": "ok"}

    menu = client.get("/api/menu")
    assert menu.status_code == 200
    assert len(menu.json()) == 16
    assert menu.json()[0]["price"] == 249.0

    bill = client.post(
        "/api/orders/calculate",
        json={"items": [{"itemId": "idli", "quantity": 2}]},
    )
    assert bill.status_code == 200
    assert bill.json()["subtotal"] == 198.0
    assert bill.json()["delivery"] == 40.0


def test_saved_order_can_be_reloaded_and_updated_with_coupon(tmp_path) -> None:
    database_path = tmp_path / "orders.sqlite3"
    client = TestClient(create_app(database_path))
    created = client.post(
        "/api/orders",
        json={"items": [{"itemId": "idli", "quantity": 2}]},
    )
    assert created.status_code == 201
    order_id = created.json()["orderId"]

    refreshed_client = TestClient(create_app(database_path))
    refreshed = refreshed_client.post(f"/api/orders/{order_id}/bill")
    assert refreshed.status_code == 200
    assert refreshed.json()["orderId"] == order_id
    assert refreshed.json()["subtotal"] == 198.0

    coupon = refreshed_client.post(
        f"/api/orders/{order_id}/coupon",
        json={"coupon": "WELCOME50"},
    )
    assert coupon.status_code == 200
    assert coupon.json()["discount"] == 50.0
    assert coupon.json()["coupon"] == "WELCOME50"

    invalid = refreshed_client.post(
        f"/api/orders/{order_id}/coupon",
        json={"coupon": "NOTREAL"},
    )
    assert invalid.status_code == 422


def test_api_validation_and_unknown_orders(tmp_path) -> None:
    client = TestClient(create_app(tmp_path / "orders.sqlite3"))
    assert client.post("/api/orders/calculate", json={"items": []}).status_code == 422
    assert (
        client.post(
            "/api/orders/calculate",
            json={"items": [{"itemId": "missing", "quantity": 1}]},
        ).status_code
        == 422
    )
    assert client.post("/api/orders/missing/bill").status_code == 404
    assert (
        client.post(
            "/api/orders/missing/coupon",
            json={"coupon": "WELCOME50"},
        ).status_code
        == 404
    )


def test_async_delivery_and_measured_benchmark_endpoints(tmp_path) -> None:
    client = TestClient(create_app(tmp_path / "orders.sqlite3"))
    availability = client.get("/api/delivery/availability?postalCode=500001")
    assert availability.status_code == 200
    assert availability.json()["checksCompleted"] == 2
    assert availability.json()["available"] is True

    benchmark = client.get("/api/performance/benchmark")
    assert benchmark.status_code == 200
    assert [entry["itemCount"] for entry in benchmark.json()["measurements"]] == [
        10,
        100,
        1000,
        10000,
    ]
    assert all(entry["elapsedMilliseconds"] >= 0 for entry in benchmark.json()["measurements"])
