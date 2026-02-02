from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import json

from psycopg.rows import dict_row
from app.db import get_connection


def log_action(
    entity_type: str,
    entity_id: int,
    action: str,
    before: dict | None,
    after: dict | None,
    actor_user_id: int | None = None,
) -> dict:
    before_json = _normalize_json(before)
    after_json = _normalize_json(after)
    before_payload = json.dumps(before_json) if before_json is not None else None
    after_payload = json.dumps(after_json) if after_json is not None else None
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO audit_log (
                    actor_user_id, entity_type, entity_id, action, before_json, after_json, timestamp
                )
                VALUES (%s, %s, %s, %s, %s::jsonb, %s::jsonb, %s)
                RETURNING id, actor_user_id, entity_type, entity_id, action, before_json, after_json, timestamp
                """,
                (
                    actor_user_id,
                    entity_type,
                    entity_id,
                    action,
                    before_payload,
                    after_payload,
                    datetime.now(timezone.utc),
                ),
            )
            row = cur.fetchone()
        conn.commit()
    return row


def list_audit(limit: int = 200) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, actor_user_id, entity_type, entity_id, action, before_json, after_json, timestamp
                FROM audit_log
                ORDER BY timestamp DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cur.fetchall()
    return rows


def _jsonable(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    if hasattr(value, "items"):
        return {k: _jsonable(v) for k, v in dict(value).items()}
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    return value


def _normalize_json(value: Any) -> Any:
    if value is None:
        return None
    cleaned = _jsonable(value)
    return json.loads(json.dumps(cleaned, default=str))
