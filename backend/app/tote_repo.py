from __future__ import annotations

from datetime import datetime

from psycopg.rows import dict_row

from app.audit_repo import log_action
from app.db import get_connection


def _next_tote_number() -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COALESCE(MAX(tote_number), 0) + 1 FROM totes")
            (value,) = cur.fetchone()
    return int(value)


def list_totes() -> list[dict]:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, tote_number, tote_name, location_id, qr_value, created_at, archived_at
                FROM totes
                WHERE archived_at IS NULL
                ORDER BY tote_number
                """
            )
            rows = cur.fetchall()
    return rows


def get_tote(tote_id: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, tote_number, tote_name, location_id, qr_value, created_at, archived_at
                FROM totes
                WHERE id = %s AND archived_at IS NULL
                """,
                (tote_id,),
            )
            row = cur.fetchone()
    return row


def create_tote(tote_name: str | None, location_id: int | None) -> dict:
    tote_number = _next_tote_number()
    qr_value = f"tote:{tote_number}"
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO totes (tote_number, tote_name, location_id, qr_value)
                VALUES (%s, %s, %s, %s)
                RETURNING id, tote_number, tote_name, location_id, qr_value, created_at, archived_at
                """,
                (tote_number, tote_name, location_id, qr_value),
            )
            row = cur.fetchone()
        conn.commit()
    log_action("tote", row["id"], "create", before=None, after=row)
    return row


def update_tote(tote_id: int, tote_name: str | None, location_id: int | None) -> dict | None:
    existing = get_tote(tote_id)
    if not existing:
        return None
    new_name = tote_name if tote_name is not None else existing["tote_name"]
    new_location_id = location_id if location_id is not None else existing["location_id"]
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                UPDATE totes
                SET tote_name = %s, location_id = %s
                WHERE id = %s
                RETURNING id, tote_number, tote_name, location_id, qr_value, created_at, archived_at
                """,
                (new_name, new_location_id, tote_id),
            )
            row = cur.fetchone()
        conn.commit()
    log_action("tote", row["id"], "update", before=existing, after=row)
    return row


def archive_tote(tote_id: int) -> dict | None:
    existing = get_tote(tote_id)
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                UPDATE totes
                SET archived_at = %s
                WHERE id = %s AND archived_at IS NULL
                RETURNING id, tote_number, tote_name, location_id, qr_value, created_at, archived_at
                """,
                (datetime.utcnow(), tote_id),
            )
            row = cur.fetchone()
        conn.commit()
    if row:
        log_action("tote", row["id"], "archive", before=existing, after=row)
    return row
