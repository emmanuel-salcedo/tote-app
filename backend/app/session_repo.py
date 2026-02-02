from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone

from psycopg.rows import dict_row

from app.db import get_connection

SESSION_TTL_HOURS = 24


def create_session(user_id: int) -> str:
    session_id = secrets.token_urlsafe(32)
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(hours=SESSION_TTL_HOURS)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sessions (id, user_id, created_at, expires_at)
                VALUES (%s, %s, %s, %s)
                """,
                (session_id, user_id, now, expires_at),
            )
        conn.commit()
    return session_id


def get_session(session_id: str) -> dict | None:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, user_id, created_at, expires_at
                FROM sessions
                WHERE id = %s
                """,
                (session_id,),
            )
            row = cur.fetchone()
    if not row:
        return None
    if row["expires_at"] and row["expires_at"] < datetime.now(timezone.utc):
        return None
    return row


def delete_session(session_id: str) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM sessions WHERE id = %s", (session_id,))
        conn.commit()
