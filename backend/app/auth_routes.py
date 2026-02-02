from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas import LoginRequest, LoginResponse, UserOut
from app.security import verify_password
from app.user_repo import get_user_by_email

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    user = get_user_by_email(payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return LoginResponse(
        ok=True,
        user=UserOut(id=user.id, email=user.email, name=user.name, role=user.role),
    )


@router.post("/logout")
def logout() -> dict:
    return {"ok": True}
