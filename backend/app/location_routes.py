from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.location_repo import archive_location, create_location, list_locations, update_location
from app.schemas import LocationCreate, LocationOut, LocationUpdate

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("", response_model=list[LocationOut])
def get_locations() -> list[LocationOut]:
    return [LocationOut(**row) for row in list_locations()]


@router.post("", response_model=LocationOut)
def create_location_route(payload: LocationCreate) -> LocationOut:
    try:
        row = create_location(name=payload.name, parent_id=payload.parent_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return LocationOut(**row)


@router.patch("/{location_id}", response_model=LocationOut)
def update_location_route(location_id: int, payload: LocationUpdate) -> LocationOut:
    try:
        row = update_location(location_id, payload.name, payload.parent_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not row:
        raise HTTPException(status_code=404, detail="Location not found")
    return LocationOut(**row)


@router.delete("/{location_id}", response_model=LocationOut)
def delete_location_route(location_id: int) -> LocationOut:
    row = archive_location(location_id)
    if not row:
        raise HTTPException(status_code=404, detail="Location not found")
    return LocationOut(**row)
