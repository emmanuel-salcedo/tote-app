from __future__ import annotations

from fastapi import APIRouter, Cookie, HTTPException, Response

from app.auth import SESSION_COOKIE
from app.schemas import LoginRequest, LoginResponse, UserOut
from app.security import verify_password
from app.session_repo import create_session, delete_session
from app.user_repo import get_user_by_email

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, response: Response) -> LoginResponse:
    user = get_user_by_email(payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    session_id = create_session(user.id)
    response.set_cookie(
        key=SESSION_COOKIE,
        value=session_id,
        httponly=True,
        samesite="lax",
    )
    return LoginResponse(
        ok=True,
        user=UserOut(id=user.id, email=user.email, name=user.name, role=user.role),
    )


@router.post("/logout")
def logout(response: Response, session_id: str | None = Cookie(default=None)) -> dict:
    if session_id:
        delete_session(session_id)
    response.delete_cookie(SESSION_COOKIE)
    return {"ok": True}
