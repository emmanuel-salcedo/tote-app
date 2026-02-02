from fastapi import FastAPI

from app.auth_routes import router as auth_router
from app.config import get_settings
from app.db import ping_db
from app.item_routes import router as item_router
from app.location_routes import router as location_router
from app.photo_routes import router as photo_router
from app.tote_routes import router as tote_router
from app.user_repo import ensure_admin
from app.user_routes import router as user_router

app = FastAPI(title="Tote Tracker API")


@app.on_event("startup")
def startup() -> None:
    settings = get_settings()
    if settings.admin_email and settings.admin_password:
        ensure_admin(settings.admin_email, settings.admin_password)


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


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(location_router)
app.include_router(tote_router)
app.include_router(item_router)
app.include_router(photo_router)
