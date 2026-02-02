from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.item_repo import list_items_by_tote
from app.schemas import ItemOut, ToteCreate, ToteOut, ToteUpdate
from app.tote_repo import archive_tote, create_tote, list_totes, update_tote

router = APIRouter(prefix="/totes", tags=["totes"])


@router.get("", response_model=list[ToteOut])
def get_totes() -> list[ToteOut]:
    return [ToteOut(**row) for row in list_totes()]


@router.post("", response_model=ToteOut)
def create_tote_route(payload: ToteCreate) -> ToteOut:
    row = create_tote(tote_name=payload.tote_name, location_id=payload.location_id)
    return ToteOut(**row)


@router.patch("/{tote_id}", response_model=ToteOut)
def update_tote_route(tote_id: int, payload: ToteUpdate) -> ToteOut:
    row = update_tote(tote_id, payload.tote_name, payload.location_id)
    if not row:
        raise HTTPException(status_code=404, detail="Tote not found")
    return ToteOut(**row)


@router.delete("/{tote_id}", response_model=ToteOut)
def delete_tote_route(tote_id: int) -> ToteOut:
    row = archive_tote(tote_id)
    if not row:
        raise HTTPException(status_code=404, detail="Tote not found")
    return ToteOut(**row)


@router.get("/{tote_id}/items", response_model=list[ItemOut])
def get_tote_items(tote_id: int) -> list[ItemOut]:
    return [ItemOut(**row) for row in list_items_by_tote(tote_id)]
