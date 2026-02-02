from __future__ import annotations

from fastapi import Cookie, HTTPException

from app.session_repo import get_session


SESSION_COOKIE = "session_id"


def require_session(session_id: str | None = Cookie(default=None)) -> dict:
    if not session_id:
        raise HTTPException(status_code=401, detail="Missing session")
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")
    return session
