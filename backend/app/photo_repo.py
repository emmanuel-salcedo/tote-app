from __future__ import annotations

import os
from datetime import datetime

from psycopg.rows import dict_row

from app.config import get_settings
from app.db import get_connection


def list_item_photos(item_id: int) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, item_id, file_path
                FROM item_photos
                WHERE item_id = %s
                ORDER BY id
                """,
                (item_id,),
            )
            rows = cur.fetchall()
    return rows


def create_item_photo(item_id: int, file_path: str) -> dict:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO item_photos (item_id, file_path)
                VALUES (%s, %s)
                RETURNING id, item_id, file_path
                """,
                (item_id, file_path),
            )
            row = cur.fetchone()
        conn.commit()
    return row


def delete_item_photo(photo_id: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                DELETE FROM item_photos
                WHERE id = %s
                RETURNING id, item_id, file_path
                """,
                (photo_id,),
            )
            row = cur.fetchone()
        conn.commit()
    return row


def ensure_upload_dir(item_id: int) -> str:
    settings = get_settings()
    base = settings.uploads_path
    item_dir = os.path.join(base, f"item_{item_id}")
    os.makedirs(item_dir, exist_ok=True)
    return item_dir
