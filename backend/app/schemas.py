from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    role: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    ok: bool
    user: UserOut | None = None


class LocationOut(BaseModel):
    id: int
    parent_id: int | None
    name: str
    path_string: str
    archived_at: datetime | None


class LocationCreate(BaseModel):
    name: str
    parent_id: int | None = None


class LocationUpdate(BaseModel):
    name: str | None = None
    parent_id: int | None = None


class ToteOut(BaseModel):
    id: int
    tote_number: int
    tote_name: str | None
    location_id: int | None
    qr_value: str
    created_at: datetime
    archived_at: datetime | None


class ToteCreate(BaseModel):
    tote_name: str | None = None
    location_id: int | None = None


class ToteUpdate(BaseModel):
    tote_name: str | None = None
    location_id: int | None = None


class ItemOut(BaseModel):
    id: int
    tote_id: int | None
    name: str
    quantity: int | None
    category: str | None
    notes: str | None
    is_checkoutable: bool
    status: str | None
    checked_out_to: str | None
    due_back_at: datetime | None
    created_at: datetime
    updated_at: datetime
    archived_at: datetime | None


class ItemCreate(BaseModel):
    tote_id: int | None = None
    name: str
    quantity: int | None = None
    category: str | None = None
    notes: str | None = None
    is_checkoutable: bool = False


class ItemUpdate(BaseModel):
    tote_id: int | None = None
    name: str | None = None
    quantity: int | None = None
    category: str | None = None
    notes: str | None = None
    is_checkoutable: bool | None = None


class ItemPhotoOut(BaseModel):
    id: int
    item_id: int
    file_path: str


class ItemCheckoutOut(BaseModel):
    id: int
    item_id: int
    checked_out_by: int | None
    checked_out_to: str | None
    checked_out_at: datetime
    due_back_at: datetime | None
    returned_at: datetime | None
    notes: str | None


class ItemCheckoutCreate(BaseModel):
    checked_out_by: int | None = None
    checked_out_to: str | None = None
    due_back_at: datetime | None = None
    notes: str | None = None


class AuditLogOut(BaseModel):
    id: int
    actor_user_id: int | None
    entity_type: str
    entity_id: int
    action: str
    before_json: dict | None
    after_json: dict | None
    timestamp: datetime


class SearchResultOut(BaseModel):
    item_id: int
    item_name: str
    quantity: int | None
    category: str | None
    notes: str | None
    tote_id: int | None
    tote_number: int | None
    tote_name: str | None
    location_path: str | None
