from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.item_repo import archive_item, create_item, list_items, update_item
from app.schemas import ItemCreate, ItemOut, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemOut])
def get_items() -> list[ItemOut]:
    return [ItemOut(**row) for row in list_items()]


@router.post("", response_model=ItemOut)
def create_item_route(payload: ItemCreate) -> ItemOut:
    row = create_item(
        tote_id=payload.tote_id,
        name=payload.name,
        quantity=payload.quantity,
        category=payload.category,
        notes=payload.notes,
        is_checkoutable=payload.is_checkoutable,
    )
    return ItemOut(**row)


@router.patch("/{item_id}", response_model=ItemOut)
def update_item_route(item_id: int, payload: ItemUpdate) -> ItemOut:
    row = update_item(
        item_id,
        payload.tote_id,
        payload.name,
        payload.quantity,
        payload.category,
        payload.notes,
        payload.is_checkoutable,
    )
    if not row:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemOut(**row)


@router.delete("/{item_id}", response_model=ItemOut)
def delete_item_route(item_id: int) -> ItemOut:
    row = archive_item(item_id)
    if not row:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemOut(**row)
