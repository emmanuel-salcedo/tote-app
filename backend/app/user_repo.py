from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from psycopg.rows import dict_row

from app.db import get_connection
from app.security import hash_password


@dataclass(frozen=True)
class User:
    id: int
    email: str
    name: str
    role: str


@dataclass(frozen=True)
class UserWithPassword(User):
    password_hash: str


def list_users() -> list[User]:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, email, name, role
                FROM users
                WHERE archived_at IS NULL
                ORDER BY id
                """
            )
            rows = cur.fetchall()
    return [User(**row) for row in rows]


def get_user_by_email(email: str) -> UserWithPassword | None:
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id, email, name, role, password_hash
                FROM users
                WHERE email = %s AND archived_at IS NULL
                """,
                (email,),
            )
            row = cur.fetchone()
    if not row:
        return None
    return UserWithPassword(**row)


def create_user(email: str, name: str, role: str, password: str) -> User:
    password_hash = hash_password(password)
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO users (email, name, role, password_hash)
                VALUES (%s, %s, %s, %s)
                RETURNING id, email, name, role
                """,
                (email, name, role, password_hash),
            )
            row = cur.fetchone()
        conn.commit()
    return User(**row)


def ensure_admin(email: str, password: str) -> User:
    existing = get_user_by_email(email)
    if existing:
        return User(id=existing.id, email=existing.email, name=existing.name, role=existing.role)
    return create_user(email=email, name="Admin", role="admin", password=password)
