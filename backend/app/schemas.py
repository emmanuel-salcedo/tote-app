from __future__ import annotations

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
