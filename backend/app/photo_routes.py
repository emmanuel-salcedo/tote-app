from __future__ import annotations

import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.auth import require_session
from app.item_repo import get_item
from app.photo_repo import create_item_photo, delete_item_photo, ensure_upload_dir, list_item_photos
from app.schemas import ItemPhotoOut

router = APIRouter(prefix="/items", tags=["photos"], dependencies=[Depends(require_session)])


@router.get("/{item_id}/photos", response_model=list[ItemPhotoOut])
def list_photos(item_id: int) -> list[ItemPhotoOut]:
    if not get_item(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return [ItemPhotoOut(**row) for row in list_item_photos(item_id)]


@router.post("/{item_id}/photos", response_model=ItemPhotoOut)
def upload_photo(item_id: int, file: UploadFile) -> ItemPhotoOut:
    if not get_item(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    ext = os.path.splitext(file.filename)[1].lower() or ".bin"
    safe_name = f"{uuid.uuid4().hex}{ext}"
    item_dir = ensure_upload_dir(item_id)
    path = os.path.join(item_dir, safe_name)

    with open(path, "wb") as out:
        out.write(file.file.read())

    row = create_item_photo(item_id=item_id, file_path=path)
    return ItemPhotoOut(**row)


@router.delete("/{item_id}/photos/{photo_id}", response_model=ItemPhotoOut)
def delete_photo(item_id: int, photo_id: int) -> ItemPhotoOut:
    row = delete_item_photo(photo_id)
    if not row or row["item_id"] != item_id:
        raise HTTPException(status_code=404, detail="Photo not found")
    try:
        os.remove(row["file_path"])
    except FileNotFoundError:
        pass
    return ItemPhotoOut(**row)
