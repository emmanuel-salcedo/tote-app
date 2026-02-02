from __future__ import annotations

from fastapi import APIRouter

from app.schemas import UserCreate, UserOut
from app.user_repo import create_user, list_users

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserOut])
def get_users() -> list[UserOut]:
    return [UserOut(**user.__dict__) for user in list_users()]


@router.post("", response_model=UserOut)
def create_user_route(payload: UserCreate) -> UserOut:
    user = create_user(
        email=payload.email,
        name=payload.name,
        role=payload.role,
        password=payload.password,
    )
    return UserOut(**user.__dict__)
