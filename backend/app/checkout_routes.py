from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.checkout_repo import check_in_item, create_checkout, get_open_checkout, list_checkouts
from app.item_repo import get_item
from app.schemas import ItemCheckoutCreate, ItemCheckoutOut

router = APIRouter(prefix="/items", tags=["checkouts"])


@router.get("/{item_id}/checkouts", response_model=list[ItemCheckoutOut])
def get_checkouts(item_id: int) -> list[ItemCheckoutOut]:
    if not get_item(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return [ItemCheckoutOut(**row) for row in list_checkouts(item_id)]


@router.post("/{item_id}/checkouts", response_model=ItemCheckoutOut)
def create_checkout_route(item_id: int, payload: ItemCheckoutCreate) -> ItemCheckoutOut:
    if not get_item(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    if get_open_checkout(item_id):
        raise HTTPException(status_code=400, detail="Item already checked out")
    row = create_checkout(
        item_id=item_id,
        checked_out_by=payload.checked_out_by,
        checked_out_to=payload.checked_out_to,
        due_back_at=payload.due_back_at,
        notes=payload.notes,
    )
    return ItemCheckoutOut(**row)


@router.post("/{item_id}/checkins", response_model=ItemCheckoutOut)
def check_in_route(item_id: int) -> ItemCheckoutOut:
    if not get_item(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    row = check_in_item(item_id)
    if not row:
        raise HTTPException(status_code=400, detail="Item is not checked out")
    return ItemCheckoutOut(**row)
