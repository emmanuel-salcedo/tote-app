from __future__ import annotations

from datetime import datetime, timezone

from psycopg.rows import dict_row

from app.audit_repo import log_action
from app.db import get_connection


def _get_location_path(parent_id: int | None, name: str) -> str:
    if parent_id is None:
        return name
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT path_string FROM locations WHERE id = %s AND archived_at IS NULL",
                (parent_id,),
            )
            row = cur.fetchone()
    if not row:
        raise ValueError("Parent location not found")
    return f"{row['path_string']} / {name}"


def list_locations() -> list[dict]:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, parent_id, name, path_string, archived_at
                FROM locations
                WHERE archived_at IS NULL
                ORDER BY path_string
                """
            )
            rows = cur.fetchall()
    return rows


def get_location(location_id: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, parent_id, name, path_string, archived_at
                FROM locations
                WHERE id = %s AND archived_at IS NULL
                """,
                (location_id,),
            )
            row = cur.fetchone()
    return row


def create_location(name: str, parent_id: int | None) -> dict:
    path_string = _get_location_path(parent_id, name)
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO locations (parent_id, name, path_string)
                VALUES (%s, %s, %s)
                RETURNING id, parent_id, name, path_string, archived_at
                """,
                (parent_id, name, path_string),
            )
            row = cur.fetchone()
        conn.commit()
    log_action("location", row["id"], "create", before=None, after=row)
    return row


def update_location(location_id: int, name: str | None, parent_id: int | None) -> dict | None:
    existing = get_location(location_id)
    if not existing:
        return None
    new_name = name or existing["name"]
    new_parent_id = parent_id if parent_id is not None else existing["parent_id"]
    path_string = _get_location_path(new_parent_id, new_name)
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                UPDATE locations
                SET parent_id = %s, name = %s, path_string = %s
                WHERE id = %s
                RETURNING id, parent_id, name, path_string, archived_at
                """,
                (new_parent_id, new_name, path_string, location_id),
            )
            row = cur.fetchone()
        conn.commit()
    log_action("location", row["id"], "update", before=existing, after=row)
    return row


def archive_location(location_id: int) -> dict | None:
    existing = get_location(location_id)
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                UPDATE locations
                SET archived_at = %s
                WHERE id = %s AND archived_at IS NULL
                RETURNING id, parent_id, name, path_string, archived_at
                """,
                (datetime.now(timezone.utc), location_id),
            )
            row = cur.fetchone()
        conn.commit()
    if row:
        log_action("location", row["id"], "archive", before=existing, after=row)
    return row
