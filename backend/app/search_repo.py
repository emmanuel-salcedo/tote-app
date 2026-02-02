from __future__ import annotations

from psycopg.rows import dict_row

from app.db import get_connection


def search_items(query: str, limit: int = 50) -> list[dict]:
    term = f"%{query}%"
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT
                    items.id AS item_id,
                    items.name AS item_name,
                    items.quantity,
                    items.category,
                    items.notes,
                    items.tote_id,
                    totes.tote_number,
                    totes.tote_name,
                    locations.path_string AS location_path
                FROM items
                LEFT JOIN totes ON items.tote_id = totes.id
                LEFT JOIN locations ON totes.location_id = locations.id
                WHERE items.archived_at IS NULL
                  AND (
                    items.name ILIKE %s OR
                    totes.tote_name ILIKE %s OR
                    CAST(totes.tote_number AS TEXT) ILIKE %s OR
                    locations.path_string ILIKE %s
                  )
                ORDER BY items.name
                LIMIT %s
                """,
                (term, term, term, term, limit),
            )
            rows = cur.fetchall()
    return rows
