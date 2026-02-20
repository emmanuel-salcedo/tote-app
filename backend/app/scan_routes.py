from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from app.auth import require_session

router = APIRouter(tags=["scan"], dependencies=[Depends(require_session)])


@router.get("/scan")
def scan_page() -> RedirectResponse:
    return RedirectResponse(url="/app#qr", status_code=307)
