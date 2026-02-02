from fastapi import FastAPI

from app.config import get_settings
from app.db import ping_db

app = FastAPI(title="Tote Tracker API")


@app.get("/")
def root() -> dict:
    settings = get_settings()
    return {
        "name": "Tote Tracker API",
        "uploads_path": settings.uploads_path,
    }


@app.get("/health")
def health() -> dict:
    settings = get_settings()
    db_ok = ping_db() if settings.database_url else False
    return {
        "status": "ok",
        "db": "ok" if db_ok else "unavailable",
    }
