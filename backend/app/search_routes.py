from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.auth import require_session
from app.search_repo import search_items
from app.schemas import SearchResultOut

router = APIRouter(prefix="/search", tags=["search"], dependencies=[Depends(require_session)])


@router.get("", response_model=list[SearchResultOut])
def search(q: str = Query(min_length=1), limit: int = Query(50, ge=1, le=200)) -> list[SearchResultOut]:
    return [SearchResultOut(**row) for row in search_items(q, limit=limit)]
