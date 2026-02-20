from __future__ import annotations

from datetime import datetime, timezone

from psycopg.rows import dict_row

from app.audit_repo import log_action
from app.db import get_connection


def list_items() -> list[dict]:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, tote_id, name, quantity, category, notes, is_checkoutable,
                       status, checked_out_to, due_back_at, created_at, updated_at, archived_at
                FROM items
                WHERE archived_at IS NULL
                ORDER BY id
                """
            )
            rows = cur.fetchall()
    return rows


def list_items_by_tote(tote_id: int) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, tote_id, name, quantity, category, notes, is_checkoutable,
                       status, checked_out_to, due_back_at, created_at, updated_at, archived_at
                FROM items
                WHERE tote_id = %s AND archived_at IS NULL
                ORDER BY id
                """,
                (tote_id,),
            )
            rows = cur.fetchall()
    return rows


def get_item(item_id: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, tote_id, name, quantity, category, notes, is_checkoutable,
                       status, checked_out_to, due_back_at, created_at, updated_at, archived_at
                FROM items
                WHERE id = %s AND archived_at IS NULL
                """,
                (item_id,),
            )
            row = cur.fetchone()
    return row


def create_item(
    tote_id: int | None,
    name: str,
    quantity: int | None,
    category: str | None,
    notes: str | None,
    is_checkoutable: bool,
) -> dict:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO items (tote_id, name, quantity, category, notes, is_checkoutable)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, tote_id, name, quantity, category, notes, is_checkoutable,
                          status, checked_out_to, due_back_at, created_at, updated_at, archived_at
                """,
                (tote_id, name, quantity, category, notes, is_checkoutable),
            )
            row = cur.fetchone()
        conn.commit()
    log_action("item", row["id"], "create", before=None, after=row)
    return row


def update_item(
    item_id: int,
    tote_id: int | None,
    name: str | None,
    quantity: int | None,
    category: str | None,
    notes: str | None,
    is_checkoutable: bool | None,
) -> dict | None:
    existing = get_item(item_id)
    if not existing:
        return None
    new_tote_id = tote_id if tote_id is not None else existing["tote_id"]
    new_name = name if name is not None else existing["name"]
    new_quantity = quantity if quantity is not None else existing["quantity"]
    new_category = category if category is not None else existing["category"]
    new_notes = notes if notes is not None else existing["notes"]
    new_is_checkoutable = (
        is_checkoutable if is_checkoutable is not None else existing["is_checkoutable"]
    )
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                UPDATE items
                SET tote_id = %s,
                    name = %s,
                    quantity = %s,
                    category = %s,
                    notes = %s,
                    is_checkoutable = %s,
                    updated_at = %s
                WHERE id = %s
                RETURNING id, tote_id, name, quantity, category, notes, is_checkoutable,
                          status, checked_out_to, due_back_at, created_at, updated_at, archived_at
                """,
                (
                    new_tote_id,
                    new_name,
                    new_quantity,
                    new_category,
                    new_notes,
                    new_is_checkoutable,
                    datetime.now(timezone.utc),
                    item_id,
                ),
            )
            row = cur.fetchone()
        conn.commit()
    log_action("item", row["id"], "update", before=existing, after=row)
    return row


def archive_item(item_id: int) -> dict | None:
    existing = get_item(item_id)
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                UPDATE items
                SET archived_at = %s
                WHERE id = %s AND archived_at IS NULL
                RETURNING id, tote_id, name, quantity, category, notes, is_checkoutable,
                          status, checked_out_to, due_back_at, created_at, updated_at, archived_at
                """,
                (datetime.now(timezone.utc), item_id),
            )
            row = cur.fetchone()
        conn.commit()
    if row:
        log_action("item", row["id"], "archive", before=existing, after=row)
    return row
