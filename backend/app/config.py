from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    database_url: str | None
    admin_email: str | None
    admin_password: str | None
    uploads_path: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv("DATABASE_URL"),
        admin_email=os.getenv("ADMIN_EMAIL"),
        admin_password=os.getenv("ADMIN_PASSWORD"),
        uploads_path=os.getenv("UPLOADS_PATH", "/uploads"),
    )
