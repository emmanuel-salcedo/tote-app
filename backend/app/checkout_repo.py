from __future__ import annotations

from datetime import datetime, timezone

from psycopg.rows import dict_row

from app.db import get_connection


def list_checkouts(item_id: int) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, item_id, checked_out_by, checked_out_to, checked_out_at,
                       due_back_at, returned_at, notes
                FROM item_checkouts
                WHERE item_id = %s
                ORDER BY checked_out_at DESC
                """,
                (item_id,),
            )
            rows = cur.fetchall()
    return rows


def get_open_checkout(item_id: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, item_id, checked_out_by, checked_out_to, checked_out_at,
                       due_back_at, returned_at, notes
                FROM item_checkouts
                WHERE item_id = %s AND returned_at IS NULL
                ORDER BY checked_out_at DESC
                LIMIT 1
                """,
                (item_id,),
            )
            row = cur.fetchone()
    return row


def create_checkout(
    item_id: int,
    checked_out_by: int | None,
    checked_out_to: str | None,
    due_back_at: datetime | None,
    notes: str | None,
) -> dict:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO item_checkouts (
                    item_id, checked_out_by, checked_out_to, checked_out_at, due_back_at, notes
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, item_id, checked_out_by, checked_out_to, checked_out_at,
                          due_back_at, returned_at, notes
                """,
                (
                    item_id,
                    checked_out_by,
                    checked_out_to,
                    datetime.now(timezone.utc),
                    due_back_at,
                    notes,
                ),
            )
            row = cur.fetchone()
        conn.commit()
    return row


def check_in_item(item_id: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                UPDATE item_checkouts
                SET returned_at = %s
                WHERE id = (
                    SELECT id FROM item_checkouts
                    WHERE item_id = %s AND returned_at IS NULL
                    ORDER BY checked_out_at DESC
                    LIMIT 1
                )
                RETURNING id, item_id, checked_out_by, checked_out_to, checked_out_at,
                          due_back_at, returned_at, notes
                """,
                (datetime.now(timezone.utc), item_id),
            )
            row = cur.fetchone()
        conn.commit()
    return row
