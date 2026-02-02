from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.auth import require_session
from app.audit_repo import list_audit
from app.schemas import AuditLogOut

router = APIRouter(prefix="/audit", tags=["audit"], dependencies=[Depends(require_session)])


@router.get("", response_model=list[AuditLogOut])
def get_audit(limit: int = Query(200, ge=1, le=500)) -> list[AuditLogOut]:
    return [AuditLogOut(**row) for row in list_audit(limit=limit)]
