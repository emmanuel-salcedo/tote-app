from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from app.auth import require_session

router = APIRouter(tags=["checkout-ui"], dependencies=[Depends(require_session)])


@router.get("/checkout")
def checkout_page() -> RedirectResponse:
    return RedirectResponse(url="/app#checkout", status_code=307)
