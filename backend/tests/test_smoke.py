from __future__ import annotations

import os
import uuid

import pytest
from fastapi.testclient import TestClient

psycopg = pytest.importorskip("psycopg")


REQUIRED_ENV = ("DATABASE_URL", "ADMIN_EMAIL", "ADMIN_PASSWORD")


def _require_env() -> None:
    missing = [key for key in REQUIRED_ENV if not os.getenv(key)]
    if missing:
        pytest.skip(f"Missing required env vars: {', '.join(missing)}")


def _reset_db(database_url: str) -> None:
    table_names = [
        "audit_log",
        "item_checkouts",
        "item_photos",
        "items",
        "totes",
        "locations",
        "sessions",
        "users",
    ]
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT to_regclass('public.users') IS NOT NULL, to_regclass('public.items') IS NOT NULL"
            )
            users_exists, items_exists = cur.fetchone()
            if not users_exists or not items_exists:
                raise AssertionError(
                    "Schema tables not found. Run: psql \"$DATABASE_URL\" -f db/migrations/0001_init.sql"
                )
            cur.execute(f"TRUNCATE TABLE {', '.join(table_names)} RESTART IDENTITY CASCADE")
        conn.commit()


@pytest.fixture()
def client() -> TestClient:
    _require_env()
    database_url = os.environ["DATABASE_URL"]
    _reset_db(database_url)

    from app.config import get_settings

    get_settings.cache_clear()

    from app.main import app

    with TestClient(app) as test_client:
        yield test_client


def test_api_smoke_flow(client: TestClient) -> None:
    suffix = uuid.uuid4().hex[:8]

    login = client.post(
        "/auth/login",
        json={
            "email": os.environ["ADMIN_EMAIL"],
            "password": os.environ["ADMIN_PASSWORD"],
        },
    )
    assert login.status_code == 200, login.text
    assert login.json()["ok"] is True

    root_location = client.post("/locations", json={"name": f"Garage-{suffix}"})
    assert root_location.status_code == 200, root_location.text
    root_location_id = root_location.json()["id"]

    shelf_location = client.post(
        "/locations",
        json={"name": f"Shelf-{suffix}", "parent_id": root_location_id},
    )
    assert shelf_location.status_code == 200, shelf_location.text
    shelf_location_id = shelf_location.json()["id"]
    assert "Garage-" in shelf_location.json()["path_string"]

    tote_a = client.post(
        "/totes",
        json={"tote_name": f"Holiday-{suffix}", "location_id": root_location_id},
    )
    assert tote_a.status_code == 200, tote_a.text
    tote_a_id = tote_a.json()["id"]

    tote_b = client.post(
        "/totes",
        json={"tote_name": f"Overflow-{suffix}", "location_id": shelf_location_id},
    )
    assert tote_b.status_code == 200, tote_b.text
    tote_b_id = tote_b.json()["id"]

    item = client.post(
        "/items",
        json={
            "name": f"Lights-{suffix}",
            "tote_id": tote_a_id,
            "quantity": 2,
            "category": "seasonal",
            "notes": "LED string lights",
            "is_checkoutable": True,
        },
    )
    assert item.status_code == 200, item.text
    item_id = item.json()["id"]

    search = client.get(f"/search?q={suffix}&limit=10")
    assert search.status_code == 200, search.text
    assert any(row["item_id"] == item_id for row in search.json())

    move_item = client.post(f"/moves/items/{item_id}", json={"tote_id": tote_b_id})
    assert move_item.status_code == 200, move_item.text
    assert move_item.json()["tote_id"] == tote_b_id

    move_tote = client.post(f"/moves/totes/{tote_b_id}", json={"location_id": root_location_id})
    assert move_tote.status_code == 200, move_tote.text
    assert move_tote.json()["location_id"] == root_location_id

    checkout = client.post(
        f"/items/{item_id}/checkouts",
        json={
            "checked_out_to": "Tester",
            "notes": "Smoke checkout",
        },
    )
    assert checkout.status_code == 200, checkout.text
    assert checkout.json()["item_id"] == item_id
    assert checkout.json()["returned_at"] is None

    checkin = client.post(f"/items/{item_id}/checkins")
    assert checkin.status_code == 200, checkin.text
    assert checkin.json()["item_id"] == item_id
    assert checkin.json()["returned_at"] is not None

    qr = client.get(f"/totes/{tote_b_id}/qr")
    assert qr.status_code == 200
    assert qr.headers.get("content-type", "").startswith("image/png")
    assert len(qr.content) > 0

    audit = client.get("/audit?limit=200")
    assert audit.status_code == 200, audit.text
    actions = {(row["entity_type"], row["action"]) for row in audit.json()}
    assert ("item", "create") in actions
    assert ("checkout", "create") in actions
    assert ("checkout", "checkin") in actions

    frontend = client.get("/app")
    assert frontend.status_code == 200
    assert "Tote Tracker" in frontend.text

    scan_redirect = client.get("/scan", follow_redirects=False)
    assert scan_redirect.status_code == 307
    assert scan_redirect.headers["location"] == "/app#qr"

    checkout_redirect = client.get("/checkout", follow_redirects=False)
    assert checkout_redirect.status_code == 307
    assert checkout_redirect.headers["location"] == "/app#checkout"
