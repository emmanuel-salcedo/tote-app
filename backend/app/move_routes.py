from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.auth import require_session
from app.item_repo import get_item, update_item
from app.schemas import ItemMoveRequest, ItemOut, ToteMoveRequest, ToteOut
from app.tote_repo import get_tote, update_tote

router = APIRouter(prefix="/moves", tags=["moves"], dependencies=[Depends(require_session)])


@router.post("/items/{item_id}", response_model=ItemOut)
def move_item(item_id: int, payload: ItemMoveRequest) -> ItemOut:
    if not get_item(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    row = update_item(
        item_id=item_id,
        tote_id=payload.tote_id,
        name=None,
        quantity=None,
        category=None,
        notes=None,
        is_checkoutable=None,
    )
    if not row:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemOut(**row)


@router.post("/totes/{tote_id}", response_model=ToteOut)
def move_tote(tote_id: int, payload: ToteMoveRequest) -> ToteOut:
    if not get_tote(tote_id):
        raise HTTPException(status_code=404, detail="Tote not found")
    row = update_tote(tote_id, tote_name=None, location_id=payload.location_id)
    if not row:
        raise HTTPException(status_code=404, detail="Tote not found")
    return ToteOut(**row)
